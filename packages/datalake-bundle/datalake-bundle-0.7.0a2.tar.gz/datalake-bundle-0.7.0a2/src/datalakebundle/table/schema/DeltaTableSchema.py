from pyspark.sql.types import StructType


class DeltaTableSchema(StructType):
    def __init__(self, fields: list, primary_key):
        if not isinstance(primary_key, str) and not isinstance(primary_key, list):
            raise Exception(f"Invalid primary key: {primary_key}")

        super().__init__(fields)
        self.__primary_key_columns = [primary_key] if isinstance(primary_key, str) else primary_key

    @property
    def primary_key_columns(self) -> list:
        return self.__primary_key_columns

    @classmethod
    def typeName(cls):  # noqa: N802
        return "struct"
