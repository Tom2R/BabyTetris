import unittest
from game import Game
from state import State


class Simulator(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_random_duel(self):
        from players import RandomPlayer

        play = RandomPlayer()

        from players import Randomselector

        sele = Randomselector()

        game = Game(player=play, selector=sele, nb_colums=8, height=8)

        game.play()

    def test_line_clearing(self):

        s = State(nb_columns=5, height=5)

        s.grid[3, 3] = False
        s.grid[2, 3] = False
        s.grid[3, 2] = False

        for x in range(s.nb_columns):
            s.grid[x, 4] = False

        # print("grid before")
        # print(s)

        cleared = s.count_number_full_lines()

        # print("grid after")
        # print(s)
        assert cleared == 1
