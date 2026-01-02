import unittest

from matplotlib import pyplot as plt
import numpy as np
from game import Game
from state import State
import time


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

    def test_vi_player_vs_vi_random_selector(self):
        from players import ValueIterationPlayer

        play = ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.9.json"
        )

        from players import ValueIterationOnRandomSelector

        sele = ValueIterationOnRandomSelector(
            reverse_cheatdict_name="reverse_cheatdict/reverse_cheatdict_0.01_0.1"
        )

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


def test_vi_player_vs_vi_random_selector(epsilon, indicator):
    """Generates a game between VI player and the VI selector
    Indicator True = VI selector built with random player
    Indicator False = VI selector built with VI player"""

    from players import ValueIterationPlayer

    play = ValueIterationPlayer(cheatdict_name="cheatdict/cheat_dict_lambda_0.6.json")

    from players import ValueIterationSelectorOnRandomPlayer

    if indicator:
        sele = ValueIterationSelectorOnRandomPlayer(
            reverse_cheatdict_name=f"reverse_cheatdict/reverse_cheatdict_random_{epsilon}_0.1"
        )
    else:
        sele = ValueIterationSelectorOnRandomPlayer(
            reverse_cheatdict_name=f"reverse_cheatdict/reverse_cheatdict_VI_{epsilon}_0.1"
        )

    game = Game(player=play, selector=sele, nb_colums=4, height=4)

    game.play()


test_vi_player_vs_vi_random_selector(0.1, False)
print("next is 0.01")
time.sleep(5)
test_vi_player_vs_vi_random_selector(0.01, False)
print("next is 0.001")
time.sleep(5)
test_vi_player_vs_vi_random_selector(0.001, False)
print("next is random")
time.sleep(5)


def test_value_iteration_vs_random():

    from players import ValueIterationPlayer

    play = ValueIterationPlayer(cheatdict_name="cheatdict/cheat_dict_lambda_0.6.json")

    from players import Randomselector

    sele = Randomselector()

    game = Game(player=play, selector=sele, nb_colums=4, height=4)

    game.play()


test_value_iteration_vs_random()
