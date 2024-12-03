from liminal.base.str_enum import StrEnum


class ValidationReportLevel(StrEnum):
    """This enum represents the different levels of validation that can be returned by Benchling."""

    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"
    UNEXPECTED = "UNEXPECTED"
