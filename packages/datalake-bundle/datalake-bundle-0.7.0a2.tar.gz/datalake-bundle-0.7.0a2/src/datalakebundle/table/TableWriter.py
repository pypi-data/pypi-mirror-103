from logging import Logger
from pyspark.sql.session import SparkSession
from pyspark.sql.dataframe import DataFrame
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.upsert.UpsertQueryCreator import UpsertQueryCreator
from datalakebundle.table.write import upsert_checker
import pyspark.sql.types as t
import yaml
import string
import random


class TableWriter:
    def __init__(
        self,
        logger: Logger,
        spark: SparkSession,
        upsert_query_creator: UpsertQueryCreator,
    ):
        self.__logger = logger
        self.__spark = spark
        self.__upsert_query_creator = upsert_query_creator

    def append(self, df: DataFrame, table_config: TableConfig):
        self.__insert_into(df, table_config, False)

    def overwrite(self, df: DataFrame, table_config: TableConfig):
        self.__insert_into(df, table_config, True)

    def upsert(self, df: DataFrame, table_config: TableConfig):
        upsert_checker.check(table_config)

        self.__check_schema(df, table_config)

        temp_source_table = f"upsert_{table_config.table_identifier}_{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}"

        df.createOrReplaceTempView(temp_source_table)

        upsert_sql_statement = self.__upsert_query_creator.create(table_config, temp_source_table)

        try:
            self.__spark.sql(upsert_sql_statement)

        except BaseException:
            raise

        finally:
            self.__spark.catalog.dropTempView(temp_source_table)

    def __check_schema(self, df: DataFrame, table_config: TableConfig):
        table_schema = table_config.schema

        def print_schema(schema: t.StructType):
            return yaml.dump(schema.jsonValue())

        def remove_metadata(json_schema):
            for field in json_schema["fields"]:
                field["metadata"] = dict()

            return json_schema

        if remove_metadata(table_schema.jsonValue()) != remove_metadata(df.schema.jsonValue()):
            error_message = "Table and dataframe schemas do NOT match"

            self.__logger.error(
                error_message,
                extra={
                    "df_schema": print_schema(df.schema),
                    "table_schema": print_schema(table_schema),
                    "table_schema_loader": table_config.schema_loader,
                    "table": table_config.full_table_name,
                },
            )

            raise Exception(error_message)

    def __insert_into(self, df: DataFrame, table_config: TableConfig, overwrite: bool):
        self.__check_schema(df, table_config)

        df.write.insertInto(table_config.full_table_name, overwrite=overwrite)
