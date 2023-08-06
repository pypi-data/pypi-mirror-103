from logging import Logger
from daipecore.decorator.DecoratedDecorator import DecoratedDecorator
from daipecore.decorator.OutputDecorator import OutputDecorator
from injecta.container.ContainerInterface import ContainerInterface


class TestingStorage:
    result: None


@DecoratedDecorator
class dummy_saver(OutputDecorator):  # noqa: N801
    def __init__(self, table_identifier: str):
        self._table_identifier = table_identifier

    def process_result(self, result, container: ContainerInterface):
        logger: Logger = container.get("datalakebundle.logger")

        logger.info(f"Saving into {self._table_identifier}")

        TestingStorage.result = result
