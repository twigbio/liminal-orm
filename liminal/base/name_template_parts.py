from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

from liminal.enums.name_template_part_type import NameTemplatePartType

if TYPE_CHECKING:
    from liminal.entity_schemas.tag_schema_models import (
        NameTemplatePartModel,
        TagSchemaFieldModel,
    )


class NameTemplatePart(BaseModel):
    component_type: ClassVar[NameTemplatePartType]

    _type_map: ClassVar[dict[NameTemplatePartType, type["NameTemplatePart"]]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._type_map[cls.component_type] = cls

    @classmethod
    def resolve_type(cls, type: NameTemplatePartType) -> type["NameTemplatePart"]:
        if type not in cls._type_map:
            raise ValueError(f"Invalid name template part type: {type}")
        return cls._type_map[type]

    def to_model_type(self, *args: Any, **kwargs: Any) -> "NameTemplatePartModel":
        raise NotImplementedError("Subclass must implement this method")


class Separator(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.SEPARATOR
    value: str

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
            text=self.value,
        )


class Text(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.TEXT
    value: str

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
            text=self.value,
        )


class CreationYear(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_YEAR

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
        )


class CreationDate(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_DATE

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
        )


class Field(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.FIELD
    wh_field_name: str

    def to_model_type(
        self, fields: list["TagSchemaFieldModel"]
    ) -> "NameTemplatePartModel":
        field = next((f for f in fields if f.systemName == self.wh_field_name), None)
        if field is None:
            raise ValueError(f"Field {self.wh_field_name} not found in fields")
        return NameTemplatePartModel(
            type=self.component_type,
            fieldId=field.id,
        )


class RegistryIdentifierNumber(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = (
        NameTemplatePartType.REGISTRY_IDENTIFIER_NUMBER
    )

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
        )


class Project(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.PROJECT

    def to_model_type(self) -> "NameTemplatePartModel":
        return NameTemplatePartModel(
            type=self.component_type,
        )
