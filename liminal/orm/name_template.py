from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from liminal.base.name_template_parts import NameTemplateParts
from liminal.base.properties.base_name_template import BaseNameTemplate


class NameTemplate(BaseNameTemplate):
    """
    This class is the validated class that is public facing and inherits from the BaseNameTemplate class.
    It has the same fields as the BaseNameTemplate class, but it is validated to ensure that the fields are valid.
    """

    parts: list[NameTemplateParts] = []
    order_name_parts_by_sequence: bool = False

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

    model_config = ConfigDict(arbitrary_types_allowed=True)
