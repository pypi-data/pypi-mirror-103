from argparse import Namespace
from logging import Logger
from pysparkbundle.filesystem.FilesystemInterface import FilesystemInterface
from datalakebundle.table.TableExistenceChecker import TableExistenceChecker
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.config.TableConfigManager import TableConfigManager
from datalakebundle.table.create.TableCreator import TableCreator
from datalakebundle.table.create.TableRecreator import TableRecreator
from datalakebundle.table.delete.TableDeleter import TableDeleter
from datalakebundle.table.identifier.fill_template import fill_template
from datalakebundle.table.optimize.TablesOptimizerCommand import TablesOptimizerCommand


class TableManager:
    def __init__(
        self,
        table_name_template: str,
        logger: Logger,
        filesystem: FilesystemInterface,
        table_config_manager: TableConfigManager,
        table_creator: TableCreator,
        table_recreator: TableRecreator,
        table_deleter: TableDeleter,
        table_existence_checker: TableExistenceChecker,
        tables_optimizer_command: TablesOptimizerCommand,
    ):
        self.__table_name_template = table_name_template
        self.__logger = logger
        self.__filesystem = filesystem
        self.__table_config_manager = table_config_manager
        self.__table_creator = table_creator
        self.__table_recreator = table_recreator
        self.__table_deleter = table_deleter
        self.__table_existence_checker = table_existence_checker
        self.__tables_optimizer_command = tables_optimizer_command

    def get_name(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        replacements = {
            **table_config.get_custom_fields(),
            **{
                "identifier": table_config.identifier,
                "db_identifier": table_config.db_identifier,
                "table_identifier": table_config.table_identifier,
            },
        }

        return fill_template(self.__table_name_template, replacements)

    def get_config(self, identifier: str) -> TableConfig:
        return self.__table_config_manager.get(identifier)

    def create(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        self.__table_creator.create(table_config)

    def create_if_not_exists(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        if self.__table_existence_checker.table_exists(table_config.db_name, table_config.table_name):
            self.__logger.info(f"Table {table_config.full_table_name} already exists, creation skipped")
            return

        self.__table_creator.create(table_config)

    def recreate_with_data_deletion(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        self.__table_recreator.recreate(table_config)

    def exists(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        return self.__table_existence_checker.table_exists(table_config.db_name, table_config.table_name)

    def delete_with_data(self, identifier: str):
        table_config = self.__table_config_manager.get(identifier)

        self.__table_deleter.delete_with_data(table_config)

    def optimize_all(self):
        self.__tables_optimizer_command.run(Namespace())
