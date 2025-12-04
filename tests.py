import unittest

from matplotlib import pyplot as plt
import numpy as np
from game import Game
from state import State


class Simulator(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)

    def test_value_iteration_vs_random(self):

        from players import ValueIterationPlayer

        play = ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.6.json"
        )

        from players import Randomselector

        sele = Randomselector()

        game = Game(player=play, selector=sele, nb_colums=4, height=4)

        game.play()

    def test_line_clearing(self):

        s = State(nb_columns=5, height=5)

        s.grid[3, 3] = False
        s.grid[2, 3] = False
        s.grid[3, 2] = False

        for x in range(s.nb_columns):
            s.grid[x, 4] = False

        cleared = s.count_number_full_lines()

        assert cleared == 1
