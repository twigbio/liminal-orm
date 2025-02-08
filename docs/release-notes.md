For full release notes, please visit the [GitHub Releases page](https://github.com/dynotx/liminal-orm/releases). Release versions follow [semantic versioning](https://semver.org/). This page will document migration steps needed for major and minor version changes.

## v2.0.0

[![github](https://img.shields.io/badge/github-release-blue)](https://github.com/dynotx/liminal-orm/releases/tag/2.0.0) [![pypi](https://img.shields.io/pypi/v/liminal-orm.svg)](https://pypi.org/project/liminal-orm/2.0.0/)

### Upgrade Steps

- PR [#88](https://github.com/dynotx/liminal-orm/pull/88): adds ability to defined name templates for entity schemas
- PR [#84](https://github.com/dynotx/liminal-orm/pull/84): adds ability to define chip naming for entity schemas
- PR [#82](https://github.com/dynotx/liminal-orm/pull/82): adds ability to define constraints for entity schemas.
    - The above PRs brings achieves 100% parity with Entity Schemas in Benchling. The guidance for migrating to v2.0.0 is to regenerate your schemas defined in code using `liminal generate-files <benchling_tenant> [<write_path>]`. This will recreate your dropdown/schema files, this time with the new properties covered by Liminal.
- PR [#68](https://github.com/dynotx/liminal-orm/pull/68): refactors how validators are done in Liminal using a decorator pattern. Refer to the [validators](https://dynotx.github.io/liminal-orm/reference/validators/) page for full details on implementation.
    - If you don't have validators defined, no action is needed! Otherwise, you will need to manually refactor your validators to use the new pattern.

## v1.1.0

[![github](https://img.shields.io/badge/github-release-blue)](https://github.com/dynotx/liminal-orm/releases/tag/1.1.0) [![pypi](https://img.shields.io/pypi/v/liminal-orm.svg)](https://pypi.org/project/liminal-orm/1.1.0/)

### Upgrade Steps

- PR [#64](https://github.com/dynotx/liminal-orm/pull/64): makes query function optional in schema classes.
    - Remove query functions from schema classes, unless you have custom logic.
- PR [#72](https://github.com/dynotx/liminal-orm/pull/72): block warehouse name changes to operations.
    - BenchlingConnetion now takes in `warehouse_access` parameter. If you do not have warehouse access on your Benchling tenant, set this to `False`.
- PR [#53](https://github.com/dynotx/liminal-orm/pull/53): move field wh name to base field props.
    - Update historical revision files with changed operation signatures.

    ```python
    # Replace UpdateEntitySchemaName with...
    UpdateEntitySchema('old_warehouse_name', 
        BaseSchemaProperties(warehouse_name='new_warehouse_name'))

    # Replace UpdateEntitySchemaFieldName with...
    UpdateEntitySchemaField('entity_schema_warehouse_name', 
        'field_warehouse_name', 
        BaseFieldProperties(warehouse_name='new_warehouse_name'))

    # CreateEntitySchemaField no longer takes wh_field_name as a parameter. 
    # Now gets passed in via BaseFieldProperties.
    CreateEntitySchemaField('entity_schema_warehouse_name', 
        BaseFieldProperties(warehouse_name='new_warehouse_name', ...))

    # CreateEntitySchema takes in a list of fields instead of dict[str, Benchling FieldProperties]
    CreateEntitySchema(BaseSchemaProperties(...), [BaseFieldProperties(...), ...])
    ```

- PR [#63](https://github.com/dynotx/liminal-orm/pull/63): numpy and pandas version tightening.
    - numpy = “^1.23.5”
    - pandas = ">=1.5.3" --> “^1.5.3"
