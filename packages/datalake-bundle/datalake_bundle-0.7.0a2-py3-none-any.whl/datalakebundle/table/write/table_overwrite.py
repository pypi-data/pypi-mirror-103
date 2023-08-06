from logging import Logger
from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from daipecore.decorator.OutputDecorator import OutputDecorator
from injecta.container.ContainerInterface import ContainerInterface
from pyspark.sql import DataFrame
from datalakebundle.table.TableManager import TableManager
from datalakebundle.table.TableWriter import TableWriter


@DecoratedDecorator
class table_overwrite(OutputDecorator):  # noqa: N801
    def __init__(self, table_identifier: str, recreate_table=False):
        self.__table_identifier = table_identifier
        self.__recreate_table = recreate_table

    def process_result(self, result: DataFrame, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")
        table_manager: TableManager = container.get(TableManager)
        table_writer: TableWriter = container.get(TableWriter)

        output_table_name = table_manager.get_name(self.__table_identifier)

        logger.info(f"Data to be written into table: {output_table_name}")

        if self.__recreate_table:
            table_manager.recreate_with_data_deletion(self.__table_identifier)
        else:
            table_manager.create_if_not_exists(self.__table_identifier)

        logger.info(f"Writing data to table: {output_table_name}")

        table_config = table_manager.get_config(self.__table_identifier)

        table_writer.overwrite(result.select([field.name for field in table_config.schema.fields]), table_config)

        logger.info(f"Data successfully written to: {output_table_name}")
