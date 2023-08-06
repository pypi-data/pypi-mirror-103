from typing import Callable, List
import json

from honu.game import Game, Tile, Player, Position, Direction, Flag, WinCondition
from honu.test_cases import ITestCase, BaseTest, FlagTestCase, OutputTestCase, LevelTestCase
from honu.display import Display

# Base class


class Honu():
    """
    Builder

    The class that can be used to spin up a game instance, similar to that of the turtle library.
    Controls the construction of the game and the display.

    This class manages more than it should in an OOP context.
    The hope however, is to make a very simple API to work with that can be configured
    via parameters instead of through the construction of the classes within this library.
    """

    def __init__(self, enable_display: bool = True, game_width: int = 15, game_height: int = 15):
        self.enable_display = enable_display
        self.screen_height = 800
        self.screen_width = 600
        self.sleep_time = 0.2

        self.game_tiles = [[Tile.EMPTY for i in range(
            game_width)] for j in range(game_height)]
        self.flags: List[Flag] = []

        self.player_start_i = game_width//2
        self.player_start_j = game_width//2
        self.player_start_dir = Direction.SOUTH

    def create_game(self):
        # Load game
        game = Game(self.game_tiles,
                    Player(self.player_start_dir, Position(
                        self.player_start_i, self.player_start_j)),
                    self.flags)
        # Run Code
        if self.enable_display:
            display = Display(game, height=self.screen_height,
                              width=self.screen_width, sleep_time=self.sleep_time)
        return game


class HonuTest():
    def __init__(self, path_to_json: str, enable_display: bool = False):
        self.enable_display = enable_display
        self.screen_height = 800
        self.screen_width = 600
        self.sleep_time = 0.2

        self.path_to_json = path_to_json

    def load_tests_from_json(self) -> List[ITestCase]:
        tests: List[ITestCase] = []

        with open(self.path_to_json) as file:
            json_dict = json.load(file)
            title = json_dict['title']
            lib_version = json_dict['libVersion']
            win_condition: WinCondition = json_dict['winCondition'].lower()
            test_cases = json_dict['testCases']

        for test_dict in test_cases:
            level_data = test_dict['levelData']
            game = self.create_game_from_level_data(level_data)

            base_test = BaseTest(test_dict['name'], game)

            if win_condition == WinCondition.GET_ALL_FLAGS.value:
                tests.append(FlagTestCase(base_test))
            elif win_condition == WinCondition.CALC_OUTPUT.value:
                tests.append(OutputTestCase(base_test, level_data['expectedOutput']))
            elif win_condition == WinCondition.MODIFY_BOARD.value:
                tests.append(LevelTestCase(base_test, level_data['expectedBoard']))
            else:
                raise ValueError(f'The win condition {win_condition} is not recognizable!')

        return tests

    def create_game_from_level_data(self, level_data):

        player_data = level_data['player']
        player = Player(Direction(player_data['dir']), Position(player_data['pos']['x'], player_data['pos']['y']))

        flags: List[Flag] = []
        for flag_data in level_data['flags']:
            flags.append(
                Flag(Position(flag_data['pos']['x'], flag_data['pos']['y'])))

        level = [[Tile(tile_string) for tile_string in string_arr] for string_arr in level_data['level']]

        return Game(level, player, flags)

    def run_test(self, code: Callable):
        # Load json
        test_cases: List[ITestCase] = self.load_tests_from_json()
        
        # e.g. ...F..
        test_status: str = ''
        failing_tests: List[ITestCase] = []

        for test_case in test_cases:
            game = test_case.base_test.game

            if self.enable_display:
                display = Display(game, height=self.screen_height,
                              width=self.screen_width, sleep_time=self.sleep_time)
            # TODO: catch exceptions
            code(game)
            if self.enable_display:
                display.close()

            if not test_case.is_passing():
                print(f'{test_case.base_test.name} ... FAIL')
                test_status += 'F'
                failing_tests.append(test_case)
            else:
                print(f'{test_case.base_test.name} ... ok')
                test_status += '.'
        
        print(test_status)
