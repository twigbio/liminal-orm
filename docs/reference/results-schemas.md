
## Results Schema: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/orm/base_results_model.py)

Below is an example of a custom results schema defined in code. All Liminal results schema classes inherit from Liminal's [BaseResultsModel](https://github.com/dynotx/liminal-orm/blob/main/liminal/orm/base_results_model.py) and uses [SQLAlchemy](https://www.sqlalchemy.org/) behind the scenes to create an ORM.

!!! note
    It is important to note that currently, Liminal does not support migrations for results schemas. The recommended workflow is to run `liminal generate-files <benchling_tenant_name> -rs` to generate the results schema files. This will generate any new results schema files from your Benchling tenant, allowing you to use them in your codebase.

    One of the main properties of results schemas is that once there is data stored within a results schema, the schema itself cannot be changed. This makes it much less frequent of an occurrence to need to update results schemas over time. Because of this, migrations for results are at a lower development priority. Reach out if this would be a valuable feature for you in order to upgrade its priority!

The properties defined in the `ResultsSchemaProperties` object and `Column` objects
correspond with the properties shown on the Benchling website. This is how Liminal defines your Benchling results schema in code.

Below, we will go through the different components of defining a results schema class.

```python
from sqlalchemy import Column as SqlColumn

from liminal.enums import BenchlingFieldType
from liminal.orm.base_results_model import BaseResultsModel
from liminal.orm.column import Column
from liminal.orm.results_schema_properties import ResultsSchemaProperties


class PizzaCookingProcess(BaseResultsModel):
    __schema_properties__ = ResultsSchemaProperties(name="Pizza Cooking Process", warehouse_name="pizza_cooking_process")

    pizza: SqlColumn = Column(name="pizza", type=BenchlingFieldType.ENTITY_LINK, required=True)
    cooking_method: SqlColumn = Column(name="cooking_method", type=BenchlingFieldType.TEXT, required=True)
    expected_cooking_time: SqlColumn = Column(name="expected_cooking_time", type=BenchlingFieldType.DECIMAL, required=True)

    def __init__(
        self,
        pizza: str,
        cooking_method: str,
        expected_cooking_time: float,
    ):
        self.pizza = pizza
        self.cooking_method = cooking_method
        self.expected_cooking_time = expected_cooking_time
```

## Data Access & Validation

If you have warehouse access, you can access data from results schemas by using [SQLAlchemy's standard query interface](https://docs.sqlalchemy.org/en/14/orm/queryguide.html) or the built in base class functions Liminal provides.

```python
from ..pizza_cooking_process import PizzaCookingProcess

# Standard SQLAlchemy query
with BenchlingService(benchling_connection, with_db=True) as session:
    all_results = session.query(PizzaCookingProcess).all()

# Liminal base class functions
with BenchlingService(benchling_connection, with_db=True) as session:
    all_results = PizzaCookingProcess.all(session)

    all_results_df = PizzaCookingProcess.df(session)

```

With warehouse access, you can also create custom validation rules and run them very easily through Liminal's validation framework (see docs [here](../reference/validation.md)).

## Components

### Schema Properties: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/orm/results_schema_properties.py)

#### Parameters

- **name: str**

    The name of the results schema. Must be unique across all results schemas.

- **warehouse_name: str**

    The warehouse name of the results schema. Must be unique across all results schemas.

### Column: [class](https://github.com/dynotx/liminal-orm/blob/main/liminal/orm/column.py)

Same as entity schemas, results schemas use the same `Column` class. Refer to the [Columns](../reference/entity-schemas.md#column) section within the entity schema reference page for more information on how to define columns.

### Relationships: [module](https://github.com/dynotx/liminal-orm/blob/main/liminal/orm/relationship.py)

Same as entity schemas, results schemas can have relationships. Refer to the [Relationships](../reference/entity-schemas.md#relationships) section within the entity schema reference page for more information on how to define SQLAlchemy relationships.
