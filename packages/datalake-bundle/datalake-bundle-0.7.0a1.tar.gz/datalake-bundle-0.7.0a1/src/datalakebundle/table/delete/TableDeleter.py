from logging import Logger
from pyspark.sql.session import SparkSession
from pysparkbundle.filesystem.FilesystemInterface import FilesystemInterface
from datalakebundle.table.TableExistenceChecker import TableExistenceChecker
from datalakebundle.table.UnknownTableException import UnknownTableException
from datalakebundle.table.config.TableConfig import TableConfig


class TableDeleter:
    def __init__(
        self,
        logger: Logger,
        filesystem: FilesystemInterface,
        table_existence_checker: TableExistenceChecker,
        spark: SparkSession,
    ):
        self.__logger = logger
        self.__filesystem = filesystem
        self.__table_existence_checker = table_existence_checker
        self.__spark = spark

    def delete_with_data(self, table_config: TableConfig):
        self.__logger.info(f"Hive table to be deleted: {table_config.full_table_name}")
        self.__logger.warning(f"Datalake files to be deleted: {table_config.target_path}")

        if self.__table_existence_checker.table_exists(table_config.db_name, table_config.table_name) is False:
            raise UnknownTableException(f"Table {table_config.full_table_name} does not exist in Hive")

        self.__spark.sql(f"DROP TABLE {table_config.full_table_name}")
        self.__filesystem.delete(table_config.target_path, True)

        self.__logger.info(f"Hive table {table_config.full_table_name} and data deleted")
