from typing import ClassVar

from pydantic import BaseModel

from liminal.enums.name_template_part_type import NameTemplatePartType


class NameTemplatePart(BaseModel):
    pass


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
    value: str


class RegistryIdentifierNumber(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = (
        NameTemplatePartType.REGISTRY_IDENTIFIER_NUMBER
    )


class Project(NameTemplatePart):
    component_type: ClassVar[NameTemplatePartType] = NameTemplatePartType.PROJECT
