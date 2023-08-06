from logging import Logger
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.TableExistenceChecker import TableExistenceChecker
from datalakebundle.table.create.EmptyDataframeWriter import EmptyDataframeWriter


class TableRecreator:
    def __init__(
        self,
        logger: Logger,
        empty_dataframe_writer: EmptyDataframeWriter,
        table_existence_checker: TableExistenceChecker,
    ):
        self.__logger = logger
        self.__empty_dataframe_writer = empty_dataframe_writer
        self.__table_existence_checker = table_existence_checker

    def recreate(self, table_config: TableConfig):
        self.__logger.info(f"Recreating table {table_config.full_table_name}")

        self.__empty_dataframe_writer.overwrite(table_config)

        self.__logger.info(f"Table {table_config.full_table_name} successfully recreated")
