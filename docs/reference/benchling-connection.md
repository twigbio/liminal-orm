## BenchlingConnection: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/connection/benchling_connection.py)

The `BenchlingConnection` class is used to define the connection information for a particular Benchling tenant. The BenchlingConnection class is defined in your `env.py` file and it also used to create a BenchlingService object. In the `env.py` file, the api_client and internal_api parameters are required for the BenchlingConnection object in orderto be used in the migration service. The BenchlingService can be imported from the liminal pacakage and be used to connect to [Benchling's SDK](https://docs.benchling.com/docs/getting-started-with-the-sdk), internal API, and/or Postgres warehouse.

```python
# Example BenchlingConnection definition
from liminal.connection import BenchlingConnection

PROD_CURRENT_REVISION_ID = "12b31776a755b"

# It is highly recommended to use a secrets manager to store your credentials.
connection = BenchlingConnection(
    tenant_name="pizzahouse-prod",
    tenant_alias="prod",
    current_revision_id_var_name="PROD_CURRENT_REVISION_ID",
    api_client_id="my-secret-api-client-id",
    api_client_secret="my-secret-api-client-secret",
    warehouse_connection_string="my-warehouse-connection-string",
    internal_api_admin_email="my-secret-internal-api-admin-email",
    internal_api_admin_password="my-secret-internal-api-admin-password",
    config_flags={...}
)
```

### Parameters

- **tenant_name: str**

    The name of the tenant. ex: {tenant_name}.benchling.com

- **tenant_alias: Optional[str] = None**

    The alias of the tenant name. This is optional and is used as an alternate value when using the Liminal CLI

- **current_revision_id_var_name: str = ""**

    The name of the variable that contains the current revision id.
    If not provided, a derived name will be generated based on the tenant name/alias.
    Ex: {tenant_alias}_CURRENT_REVISION_ID or {tenant_name}_CURRENT_REVISION_ID if alias is not provided.

- **api_client_id: Optional[str] = None**

    The id of the API client.

- **api_client_secret: Optional[str] = None**

    The secret of the API client.

- **warehouse_connection_string: Optional[str] = None**

    The connection string for the warehouse.

- **internal_api_admin_email: Optional[str] = None**

    The email of the internal API admin.

- **internal_api_admin_password: Optional[str] = None**

    The password of the internal API admin.

- **fieldsets: bool = False**

    Whether your Benchling tenant has access to fieldsets.

- **config_flags: Optional[TenantConfigFlags] = None**

    Set of config flags that are configured on the tenant level, that defines specific features of the tenant. These can be updated on Benchling's end by contacting their support team.

### TenantConfigFlags

Set of config flags that are configured on the tenant level. These can be updated on Benchling's end by contacting their support team.
Ask Benchling support to give you the full export of these flags.

- **schemas_enable_change_warehouse_name: bool | None = None**

    If set to True, allows renaming schema and field warehouse names for all schema admins. If set to False, operations will raise an error at the validation step if the warehouse name is tried to be updated. Default value is False for Benchling.

    !!! note
        Liminal assumes the Benchling generated warehouse names to be `to_snake_case(name)`.
