from logging import Logger
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.TableExistenceChecker import TableExistenceChecker
from datalakebundle.table.create.EmptyDataframeWriter import EmptyDataframeWriter


class TableCreator:
    def __init__(
        self,
        logger: Logger,
        empty_dataframe_writer: EmptyDataframeWriter,
        table_existence_checker: TableExistenceChecker,
    ):
        self.__logger = logger
        self.__empty_dataframe_writer = empty_dataframe_writer
        self.__table_existence_checker = table_existence_checker

    def create(self, table_config: TableConfig):
        if self.__table_existence_checker.table_exists(table_config.db_name, table_config.table_name):
            raise Exception(f"Hive table {table_config.full_table_name} already exists")

        self.__logger.info(f"Creating new table {table_config.full_table_name} for {table_config.target_path}")

        self.__empty_dataframe_writer.write_errorifexists(table_config)

        self.__logger.info(f"Table {table_config.full_table_name} successfully created")
