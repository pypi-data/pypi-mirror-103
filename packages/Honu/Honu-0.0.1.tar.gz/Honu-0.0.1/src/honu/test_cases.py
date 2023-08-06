from abc import abstractmethod, ABCMeta
from typing import Any, Callable, List
from honu.game import Game, Tile


# class TestSuite():
#     screen

class BaseTest():
    def __init__(self, name: str, game: Game):
        self.name = name
        self.game = game


class ITestCase(metaclass=ABCMeta):
    def __init__(self, base_test: BaseTest):
        self.base_test = base_test

    @abstractmethod
    def is_passing(self):
        pass


class LevelTestCase(ITestCase):
    def __init__(self, base_test: BaseTest, expected_level: List[List[Tile]]):
        self.base_test = base_test
        self.expected_level = expected_level

    def is_passing(self):
        return self.base_test.game.level == expected_level


class OutputTestCase(ITestCase):
    def __init__(self, base_test: BaseTest, expected_output: Any):
        self.base_test = base_test
        self.expected_output = expected_output

    def is_passing(self):
        return self.base_test.game.output == expected_output


class FlagTestCase(ITestCase):
    def __init__(self, base_test: BaseTest):
        self.base_test = base_test

    def is_passing(self):
        return len(self.base_test.game.flags) == 0
