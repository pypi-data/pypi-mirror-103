from honu.game import Game, Tile, Player, Position, Direction, Flag
from honu.display import Display


def create_game():
    game = Game([[Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
                 [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
                 [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
                 [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
                 [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]],
                Player(Direction.SOUTH, Position(0, 0)),
                [Flag(Position(2, 2))])
    display = Display(game, height=800, width=600, sleep_time=0.2)
    return game

# def load_test():
