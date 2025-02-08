When using Benchling to store essential data, it is important to validate the data to ensure accuracy and consistency. Liminal provides an easy way to define "validators" on entity schemas that ensure entities adhere to your defined business logic. These validators can be run easily by calling the `validate()` method on the entity schema.

!!! note
    Warehouse access is required to run validators.

## Defining a Liminal Validator [decorator](https://github.com/dynotx/liminal-orm/blob/main/liminal/validation/__init__.py#L61)

Any functions decorated with `liminal_validator` are detected as validators for the entity schema.
Each validator returns a `BenchlingValidatorReport` object per entity it is run on, with either `valid=True` or `valid=False`.
If no errors are raised when it is run on an entity, the report will be valid. If an error is raised, the report will be invalid.

```python
from liminal.validation import ValidationSeverity, liminal_validator

class Pizza(BaseModel, CustomEntityMixin):
    ...

    @liminal_validator(ValidationSeverity.MED)
    def cook_time_and_temp_validator(self) -> None:
        if self.cook_time is not None and self.cook_temp is None:
            raise ValueError("Cook temp is required if cook time is set")
        if self.cook_time is None and self.cook_temp is not None:
            raise ValueError("Cook time is required if cook temp is set")
```

### Parameters

- **validator_level: ValidationSeverity**

    The severity of the validator. Defaults to `ValidationSeverity.LOW`.

- **validator_name: str | None**

    The name of the validator. Defaults to converting the function name to PascalCase.

## Running Validation

To run validation using Liminal, call the `validate()` method on the entity schema:

```python
with BenchlingSession(benchling_connection, with_db=True) as session:
    reports = Pizza.validate(session, only_invalid=True)
```

!!! tip
    The `validate_to_df` method returns a pandas DataFrame with all the reports. For example:

    ```python
    with BenchlingSession(benchling_connection, with_db=True) as session:
        df = Pizza.validate_to_df(session, only_invalid=True)
    ```

### Parameters

- **session : Session**

    The Benchling database session.

- **base_filters: BaseValidatorFilters | None**

    Filters to apply to the query.

- **only_invalid: bool**

    If `True`, only returns reports for entities that failed validation.

### Returns

- **list[BenchlingValidatorReport]**

    List of reports from running all validators on all entities returned from the query.

## BenchlingValidatorReport: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/validation/__init__.py#L13

These reports are filled out by the `liminal_validator` decorator behind the scenes.

### Parameters

- **valid : bool**

    Indicates whether the validation passed or failed.

- **model : str**

    The name of the model being validated. (eg: Pizza)

- **level : ValidationSeverity**

    The severity level of the validation report.

- **validator_name : str | None**

    The name of the validator that generated this report. (eg: CookTimeAndTempValidator)

- **entity_id : str | None**

    The entity ID of the entity being validated.

- **registry_id : str | None**

    The registry ID of the entity being validated.

- **entity_name : str | None**

    The name of the entity being validated.

- **message : str | None**

    A message describing the result of the validation.

- **creator_name : str | None**

    The name of the creator of the entity being validated.

- **creator_email : str | None**

    The email of the creator of the entity being validated.

- **updated_date : datetime | None**

    The date the entity was last updated.

## BaseValidatorFilters: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/base/base_validation_filters.py)

This class is used to pass base filters to benchling warehouse database queries.
These columns are found on all tables in the benchling warehouse database.

### Parameters

- **created_date_start: date | None**

    Start date for created date filter.

- **created_date_end: date | None**

    End date for created date filter.

- **updated_date_start: date | None**

    Start date for updated date filter.

- **updated_date_end: date | None**

    End date for updated date filter.

- **entity_ids: list[str] | None**

    List of entity IDs to filter by.

- **creator_full_names: list[str] | None**

    List of creator full names to filter by.
