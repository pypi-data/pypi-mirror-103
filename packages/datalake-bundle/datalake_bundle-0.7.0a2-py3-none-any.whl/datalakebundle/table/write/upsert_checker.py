from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.schema.DeltaTableSchema import DeltaTableSchema


def check(table_config: TableConfig):
    if not isinstance(table_config.schema, DeltaTableSchema):
        raise Exception("To perform upsert, table schema must be defined as DeltaTableSchema instead of StructType")
