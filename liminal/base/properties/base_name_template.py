from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from liminal.base.name_template_parts import NameTemplatePart


class BaseNameTemplate(BaseModel):
    """
    This class is the generic class for defining the name template.
    It is used to create a diff between the old and new name template.

    Parameters
    ----------
    parts : list[NameTemplatePart] | None
        The list of name template parts that make up the name template.
    order_name_parts_by_sequence : bool | None
        Whether to order the name parts by sequence.
    """

    parts: list[NameTemplatePart] | None = None
    order_name_parts_by_sequence: bool | None = None

    def __init__(self, **data: Any):
        super().__init__(**data)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def merge(self, new_props: BaseNameTemplate) -> dict[str, Any]:
        """Creates a diff between the current name template and the new name template.
        Sets value to None if the values are equal, otherwise sets the value to the new value.

        Parameters
        ----------
        new_props : BaseNameTemplate
            The new name template.

        Returns
        -------
        dict[str, Any]
            A dictionary of the differences between the old and new name template.
        """
        diff = {}
        for new_field_name, new_val in new_props.model_dump().items():
            if getattr(self, new_field_name) != new_val:
                diff[new_field_name] = new_val
        return diff

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseNameTemplate):
            return False
        return self.model_dump() == other.model_dump()

    def __str__(self) -> str:
        return ", ".join(
            [f"{k}={v}" for k, v in self.model_dump(exclude_unset=True).items()]
        )

    def __repr__(self) -> str:
        """Generates a string representation of the class so that it can be executed."""
        return f"{self.__class__.__name__}({', '.join([f'{k}={v.__repr__()}' for k, v in self.model_dump(exclude_unset=True).items()])})"
