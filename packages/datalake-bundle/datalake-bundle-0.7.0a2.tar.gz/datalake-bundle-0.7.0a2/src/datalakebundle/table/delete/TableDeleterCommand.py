import sys
from argparse import ArgumentParser, Namespace
from logging import Logger
from time import sleep
from consolebundle.ConsoleCommand import ConsoleCommand
from datalakebundle.table.UnknownTableException import UnknownTableException
from datalakebundle.table.config.TableConfigManager import TableConfigManager
from datalakebundle.table.delete.TableDeleter import TableDeleter
from datalakebundle.table.table_action_command import table_action_command


@table_action_command
class TableDeleterCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        table_config_manager: TableConfigManager,
        table_deleter: TableDeleter,
    ):
        self._logger = logger
        self._table_config_manager = table_config_manager
        self._table_deleter = table_deleter

    def get_command(self) -> str:
        return "datalake:table:delete-with-data"

    def get_description(self):
        return "Deletes a Hive table including all data"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="identifier", help="Table identifier")
        argument_parser.add_argument(
            "-s",
            "--skip-countdown",
            action="store_true",
            help="Skip data deletion countdown",
        )

    def run(self, input_args: Namespace):
        if input_args.skip_countdown is False:
            self._logger.info("Use the --skip-countdown switch to delete existing data immediately")

            countdown = 10

            for i in range(countdown):
                self._logger.warning(f"Data will be deleted in {countdown - i}s. Use CTRL+C to cancel.")
                sleep(1)

        table_config = self._table_config_manager.get(input_args.identifier)

        try:
            self._table_deleter.delete_with_data(table_config)
        except UnknownTableException as e:
            self._logger.error(str(e))
            sys.exit(1)
