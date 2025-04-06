import logging
from typing import Any

import requests
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2
from benchling_sdk.benchling import Benchling
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.helpers.serialization_helpers import fields as benchling_fields
from benchling_sdk.models import CustomEntity, CustomEntityCreate, CustomEntityUpdate
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, configure_mappers
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from liminal.base.properties.base_field_properties import BaseFieldProperties
from liminal.base.properties.base_schema_properties import BaseSchemaProperties
from liminal.connection.benchling_connection import BenchlingConnection
from liminal.enums import (
    BenchlingEntityType,
    BenchlingFieldType,
    BenchlingNamingStrategy,
)

logger = logging.getLogger(__name__)

REMOTE_LIMINAL_ENTITY_NAME = "_LIMINAL_REVISION_STATE"
LIMINAL_SCHEMA_NAME = "_LIMINAL"


class BenchlingService(Benchling):
    """
    Class that creates a connection object that can be used to connect to Benchling's API, database, or internal API.
    This inherits from LiminalBenchlingService, which takes in credentials and connects the specified services.

    Parameters
    ----------
    connection: BenchlingConnection
        The connection object that contains the credentials for the Benchling tenant.
    use_api: bool
        Whether to connect to the Benchling SDK. Requires api_client_id and api_client_secret from the connection object.
    use_db: bool = False
        Whether to connect to the Benchling Postgres database. Requires warehouse_connection_string from the connection object.
    use_internal_api: bool = False
        Whether to connect to the Benchling internal API. Requires internal_api_admin_email and internal_api_admin_password from the connection object.
    """

    def __init__(
        self,
        connection: BenchlingConnection,
        use_api: bool = True,
        use_db: bool = False,
        use_internal_api: bool = False,
    ) -> None:
        self.connection = connection
        self._session: Session | None = None
        self.use_api = use_api
        self.benchling_tenant = connection.tenant_name
        if use_api:
            retry_strategy = RetryStrategy(max_tries=10)
            auth_method = ClientCredentialsOAuth2(
                client_id=connection.api_client_id,
                client_secret=connection.api_client_secret,
                token_url=f"https://{connection.tenant_name}.benchling.com/api/v2/token",
            )
            url = f"https://{connection.tenant_name}.benchling.com"
            super().__init__(
                url=url, auth_method=auth_method, retry_strategy=retry_strategy
            )
            logger.info(f"Tenant {connection.tenant_name}: Connected to Benchling API.")
        self.use_db = use_db
        if use_db:
            if connection.warehouse_connection_string:
                self.engine: Engine = create_engine(
                    connection.warehouse_connection_string
                )
                configure_mappers()
                logger.info(
                    f"Tenant {connection.tenant_name}: Connected to Benchling read-only Postgres warehouse."
                )
            else:
                raise ValueError(
                    "use_db is True but warehouse_connection_string not provided in BenchlingConnection."
                )
        self.use_internal_api = use_internal_api
        if use_internal_api:
            if (
                connection.internal_api_admin_email
                and connection.internal_api_admin_password
            ):
                csrf_token, session = self.autogenerate_auth(
                    connection.tenant_name,
                    connection.internal_api_admin_email,
                    connection.internal_api_admin_password,
                )
                self.custom_post_cookies = {
                    "session": session,
                }
                self.custom_post_headers = {
                    "X-Csrftoken": csrf_token,
                    "Referer": f"https://{connection.tenant_name}.benchling.com/",
                    "Content-Type": "application/json",
                }
                logger.info(
                    f"Tenant {connection.tenant_name}: Connected to Benchling internal API."
                )
            else:
                raise ValueError(
                    "use_internal_api is True but internal_api_admin_email and internal_api_admin_password not provided in BenchlingConnection."
                )

    @property
    def session(self) -> Session:
        """Returns a session made by the sessionmaker"""
        return self.get_session()

    @property
    def registry_id(self) -> str:
        # This assumes there is only one registry (which has always been the case at DynoTx)
        registries = self.registry.registries()
        assert len(registries) == 1
        return registries[0].id

    def __enter__(self) -> Session:
        self._session = self.get_session()
        return self._session

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_val:
            self._session.rollback()
        self._session.close()
        self._session = None

    def get_session(self) -> Session:
        """Provides a wrapper around getting sessions which enables batch inserts"""
        if not self.use_db:
            raise ValueError(
                "Database connection not initialized! Initialize with 'use_db = True'"
            )
        session = Session(self.engine)
        session.info["environment"] = self.connection.tenant_name
        return session

    def cleanup(self) -> None:
        """Closes all sessions and cleans up engine"""
        self.engine.dispose()

    def get_remote_revision_id(self) -> str:
        """
        Uses Benchling SDK to search for the liminal entity stored in Benchling tenant.
        This contains the remote revision_id, or the revision_id that your tenant is currently on.

        Returns the remote revision_id stored on the entity.
        """
        revision_id_entities = [
            e
            for es in list(self.custom_entities.list(name=REMOTE_LIMINAL_ENTITY_NAME))
            for e in es
        ]
        if len(revision_id_entities) == 1:
            revision_id_value = revision_id_entities[0].fields["revision_id"].value
            assert type(revision_id_value) is str
            return revision_id_value
        elif len(revision_id_entities) == 0:
            raise ValueError(
                f"Did not find any entity with name '{REMOTE_LIMINAL_ENTITY_NAME}' in registry {self.registry_id}. Run a liminal migration to populate your registry with the Liminal entity that stores the remote revision_id."
            )
        else:
            raise ValueError(
                f"Found multiple entities with name '{REMOTE_LIMINAL_ENTITY_NAME}'. Archive all but one for Liminal to use. Ids found: {[e.id for e in revision_id_entities]}"
            )

    def upsert_remote_revision_id(self, revision_id: str) -> CustomEntity:
        """Updates or inserts a remote Liminal entity into your tenant with the given revision_id.
        If correct remote liminal entity is found, updates the enitity. If no entity is found, create the _LIMINAL entity schema if that doesn't exist,
        then create the remote liminal entity with the _LIMINAL schema. Upsert is needed to migrate users from using the CURRENT_REVISION_ID stored in the env.py
        file smoothly to storing in Benchling itself.

        Parameters
        ----------
        revision_id : str
            revision_id of migration file to set in Benchling on remote liminal entity.

        Returns
        -------
        CustomEntity
            remote liminal entity with updated revision_id field.
        """
        revision_id_entities = [
            e
            for es in list(self.custom_entities.list(name=REMOTE_LIMINAL_ENTITY_NAME))
            for e in es
        ]
        if len(revision_id_entities) == 1:
            # Update _LIMINAL_REVISION_STATE entity with given revision_id.
            liminal_entity = revision_id_entities[0]
            self.custom_entities.update(
                liminal_entity.id,
                CustomEntityUpdate(
                    fields=benchling_fields({"revision_id": {"value": revision_id}})
                ),
            )
            return liminal_entity
        elif len(revision_id_entities) == 0:
            # No _LIMINAL_REVISION_STATE entity found.
            schemas = [s for ss in list(self.schemas.list_entity_schemas()) for s in ss]
            if len([s for s in schemas if s.name == {LIMINAL_SCHEMA_NAME}]) == 0:
                # No _LIMINAL schema found. Create schema.
                from liminal.entity_schemas.operations import CreateEntitySchema

                CreateEntitySchema(
                    schema_properties=BaseSchemaProperties(
                        name={LIMINAL_SCHEMA_NAME},
                        warehouse_name={LIMINAL_SCHEMA_NAME.lower()},
                        prefix={LIMINAL_SCHEMA_NAME},
                        entity_type=BenchlingEntityType.CUSTOM_ENTITY,
                        naming_strategies={BenchlingNamingStrategy.NEW_IDS},
                    ),
                    fields=[
                        BaseFieldProperties(
                            name="revision_id",
                            warehouse_name="warehouse_name",
                            type=BenchlingFieldType.TEXT,
                            parent_link=False,
                            is_multi=False,
                            required=True,
                        )
                    ],
                ).execute(self)
                schemas = [
                    s for ss in list(self.schemas.list_entity_schemas()) for s in ss
                ]
            # Create new _LIMINAL_REVISION_STATE entity with given revision_id.
            liminal_schemas = [s for s in schemas if s.name == "_LIMINAL"]
            assert len(liminal_schemas) == 1
            liminal_schema = liminal_schemas[0]
            liminal_entity = self.custom_entities.create(
                CustomEntityCreate(
                    schema_id=liminal_schema.id,
                    entity_registry_id=self.registry_id,
                    registry_id=self.registry_id,
                    name=REMOTE_LIMINAL_ENTITY_NAME,
                    fields=benchling_fields({"revision_id": {"value": revision_id}}),
                )
            )
            return liminal_entity
        else:
            raise ValueError(
                f"Found multiple entities with name '{REMOTE_LIMINAL_ENTITY_NAME}'. Archive all but one for Liminal to use. Ids found: {[e.id for e in revision_id_entities]}"
            )

    @classmethod
    @retry(
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(ValueError),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def autogenerate_auth(
        cls, benchling_tenant: str, email: str, password: str
    ) -> tuple[str, str]:
        with requests.Session() as session:
            homepage = session.get(f"https://{benchling_tenant}.benchling.com/signin")
            soup = BeautifulSoup(homepage.content, features="lxml")
            input = soup.find(id="csrf_token")
            csrf_token = input.get("value")
            assert isinstance(csrf_token, str)
            login_payload = {
                "csrf_token": csrf_token,
                "username": email,
                "password": password,
                "signout_on_close": "y",
            }
            signin_response = session.post(
                f"https://{benchling_tenant}.benchling.com/signin",
                data=login_payload,
                headers={
                    "Referer": f"https://{benchling_tenant}.benchling.com/signin",
                },
            )
            if not signin_response.ok:
                raise ValueError(
                    f"Failed to sign in to Benchling: {signin_response.text}"
                )
            if not signin_response.headers.get("Set-Cookie"):
                raise ValueError(
                    f"Failed to sign in to Benchling: {signin_response.text}"
                )
            return csrf_token, signin_response.headers["Set-Cookie"].split("; Secure")[
                0
            ].removeprefix("session=")
