from pyspark.sql import SparkSession
from datalakebundle.table.config.TableConfig import TableConfig


class EmptyDataframeWriter:
    def __init__(
        self,
        spark: SparkSession,
    ):
        self.__spark = spark

    def write_errorifexists(self, table_config: TableConfig):
        self.__write(table_config, "errorifexists", {})

    def overwrite(self, table_config: TableConfig):
        options = {"overwriteSchema": "true"}

        self.__write(table_config, "overwrite", options)

    def __write(self, table_config: TableConfig, mode: str, options: dict):
        empty_df = self.__spark.createDataFrame([], table_config.schema)

        (
            empty_df.write.partitionBy(table_config.partition_by)
            .format("delta")
            .options(**options)
            .mode(mode)
            .saveAsTable(table_config.full_table_name, path=table_config.target_path)
        )
