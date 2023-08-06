from argparse import ArgumentParser, Namespace
from logging import Logger
from time import sleep
from consolebundle.ConsoleCommand import ConsoleCommand
from pysparkbundle.filesystem.FilesystemInterface import FilesystemInterface
from datalakebundle.table.config.TableConfigManager import TableConfigManager
from datalakebundle.table.create.TableRecreator import TableRecreator
from datalakebundle.table.table_action_command import table_action_command


@table_action_command
class TableRecreatorCommand(ConsoleCommand):
    def __init__(
        self,
        logger: Logger,
        filesystem: FilesystemInterface,
        table_config_manager: TableConfigManager,
        table_recreator: TableRecreator,
    ):
        self._logger = logger
        self._filesystem = filesystem
        self._table_config_manager = table_config_manager
        self._table_recreator = table_recreator

    def get_command(self) -> str:
        return "datalake:table:recreate"

    def get_description(self):
        return "Recreates a table based on it's YAML definition (name, schema, data path, ...)"

    def configure(self, argument_parser: ArgumentParser):
        argument_parser.add_argument(dest="identifier", help="Table identifier")
        argument_parser.add_argument(
            "-s",
            "--skip-countdown",
            action="store_true",
            help="Skip data deletion countdown",
        )

    def run(self, input_args: Namespace):
        table_config = self._table_config_manager.get(input_args.identifier)

        if input_args.skip_countdown is False and self._filesystem.exists(table_config.target_path):
            self._logger.info("Use the --skip-countdown switch to delete existing data immediately")

            countdown = 10

            for i in range(countdown):
                self._logger.warning(f"Data will be deleted in {countdown - i}s. Use CTRL+C to cancel.")
                sleep(1)

        self._table_recreator.recreate(table_config)
