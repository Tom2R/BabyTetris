import unittest

from matplotlib import pyplot as plt
import numpy as np
from game import Game
from players import LineEliminator
from state import Piece, PlayerAction, State
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

        game.play(visualisation=False)

    def test_vi_player_vs_vi_selector_on_random_player(self):
        from players import ValueIterationPlayer

        play = ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.9.json"
        )

        from players import ValueIterationSelectorOnRandomPlayer

        sele = ValueIterationSelectorOnRandomPlayer(
            vi_player=True, epsilon=0.01, lambd=0.1
        )

        game = Game(player=play, selector=sele, nb_colums=4, height=4)

        game.play(visualisation=False)

    def test_compact_player_vs_random(self):

        from players import CompactPlayer

        play = CompactPlayer()
        from players import Randomselector

        sele = Randomselector()
        game = Game(player=play, selector=sele, nb_colums=4, height=4)

        game.play(visualisation=False)

    def test_LineEliminator_player_vs_random(self):

        from players import CompactPlayer

        play = LineEliminator()
        from players import Randomselector

        sele = Randomselector()
        game = Game(player=play, selector=sele, nb_colums=4, height=4)

        game.play(visualisation=False)

    def test_robust_player_vs_random(self):

        from players import RobustPlayer

        play = RobustPlayer()
        from players import Randomselector

        sele = Randomselector()

        game = Game(player=play, selector=sele, nb_colums=4, height=4)

        game.play(visualisation=False)

    def test_greedy_selector_vs_vi_player(self):
        from players import GreedySelector, ValueIterationPlayer

        play = ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.5.json"
        )
        sele = GreedySelector()

        game = Game(4, 4, player=play, selector=sele)

        game.play(visualisation=True)

    def test_line_clearing(self):

        state = State(nb_columns=5, height=5)

        state.grid[3, 3] = False
        state.grid[2, 3] = False
        state.grid[3, 2] = False

        for x in range(state.nb_columns):
            state.grid[x, 4] = False

        cleared = state.count_number_full_lines()

        assert cleared == 1

    def test_count_nb_borders(self):

        state_1 = State(nb_columns=4, height=4)

        state_1.grid[3, 3] = False
        state_1.grid[2, 3] = False
        state_1.grid[3, 2] = False

        nb_borders = state_1.compute_nb_borders(
            incomming_piece=Piece(name="square", shape=np.array([[1, 1], [1, 0]])),
            action=PlayerAction(nb_rotations=0, abscisse=1),
        )

        assert nb_borders == 4

        state_2 = State(nb_columns=4, height=4)

        nb_borders = state_2.compute_nb_borders(
            incomming_piece=Piece(name="line", shape=np.array([[1, 1, 1]])),
            action=PlayerAction(nb_rotations=1, abscisse=0),
        )

        assert nb_borders == 4

        state_3 = State(nb_columns=4, height=4)

        state_3.grid[0, 3] = False
        state_3.grid[1, 3] = False
        state_3.grid[3, 3] = False

        state_3.grid[0, 2] = False
        state_3.grid[3, 2] = False

        nb_borders = state_3.compute_nb_borders(
            incomming_piece=Piece(name="square", shape=np.array([[1, 1], [1, 0]])),
            action=PlayerAction(nb_rotations=1, abscisse=1),
        )

        assert nb_borders == 6


###    Tests en dehors du module test   ###


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

    game.play(visualisation=False)


# test_vi_player_vs_vi_random_selector(0.1, True)
# test_vi_player_vs_vi_random_selector(0.01, True)
# test_vi_player_vs_vi_random_selector(0.001, True)


def test_value_iteration_vs_random():

    from players import ValueIterationPlayer

    play = ValueIterationPlayer(cheatdict_name="cheatdict/cheat_dict_lambda_0.6.json")

    from players import Randomselector

    sele = Randomselector()

    game = Game(player=play, selector=sele, nb_colums=4, height=4)

    game.play(visualisation=False)


# test_value_iteration_vs_random()


def test_compact_player_vs_random():

    from players import CompactPlayer

    play = CompactPlayer()
    from players import Randomselector

    sele = Randomselector()
    game = Game(player=play, selector=sele, nb_colums=4, height=4)

    game.play(visualisation=False)


# test_compact_player_vs_random()


def test_greedy_selector_vs_vi_player():
    from players import GreedySelector, ValueIterationPlayer

    play = ValueIterationPlayer(cheatdict_name="cheatdict/cheat_dict_lambda_0.5.json")
    sele = GreedySelector()

    game = Game(4, 4, player=play, selector=sele)

    game.play(visualisation=False)


# test_greedy_selector_vs_vi_player()
