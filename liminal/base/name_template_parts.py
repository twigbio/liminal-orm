from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, field_validator

from liminal.enums.name_template_part_type import NameTemplatePartType


class NameTemplatePart(BaseModel):
    component_type: ClassVar[NameTemplatePartType]

    _type_map: ClassVar[dict[NameTemplatePartType, type["NameTemplatePart"]]] = {}

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls._type_map[cls.component_type] = cls

    @classmethod
    def resolve_type(cls, type: NameTemplatePartType) -> type["NameTemplatePart"]:
        if type not in cls._type_map:
            raise ValueError(f"Invalid name template part type: {type}")
        return cls._type_map[type]


class SeparatorPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.SEPARATOR
    value: str

    @field_validator("value")
    def validate_value(cls, v: str) -> str:
        if not v:
            raise ValueError("value cannot be empty")
        return v


class TextPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.TEXT
    value: str

    @field_validator("value")
    def validate_value(cls, v: str) -> str:
        if not v:
            raise ValueError("value cannot be empty")
        return v


class CreationYearPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_YEAR


class CreationDatePart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_DATE


class FieldPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.FIELD
    wh_field_name: str


class ParentLotNumberPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = (
        NameTemplatePartType.CHILD_ENTITY_LOT_NUMBER
    )
    wh_field_name: str


class RegistryIdentifierNumberPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = (
        NameTemplatePartType.REGISTRY_IDENTIFIER_NUMBER
    )


class ProjectPart(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.PROJECT


NameTemplateParts = (
    SeparatorPart
    | TextPart
    | CreationYearPart
    | CreationDatePart
    | FieldPart
    | RegistryIdentifierNumberPart
    | ProjectPart
    | ParentLotNumberPart
)
