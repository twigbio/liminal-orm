from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict

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


class Separator(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.SEPARATOR
    value: str


class Text(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.TEXT
    value: str


class CreationYear(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_YEAR


class CreationDate(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.CREATION_DATE


class Field(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.FIELD
    wh_field_name: str


class RegistryIdentifierNumber(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = (
        NameTemplatePartType.REGISTRY_IDENTIFIER_NUMBER
    )


class Project(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.PROJECT


NameTemplateParts = (
    Separator
    | Text
    | CreationYear
    | CreationDate
    | Field
    | RegistryIdentifierNumber
    | Project
)
