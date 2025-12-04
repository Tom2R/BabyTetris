from copy import deepcopy
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import time

import numpy as np

from state import Piece, PlayerAction, State


def value_iteration(epsilon: float = 0.7, lamb: float = 0.8):
    """
    Execute the value iteration algorithm.
    Returns: a dict[(State,piece)]=ActionPlayer that can be used by players as a strategy.
    """

    from game import Game
    from players import RandomPlayer, Randomselector

    game = Game(player=RandomPlayer(), selector=Randomselector, nb_colums=4, height=4)
    t1 = time.time()
    delta = float("inf")
    from fichier_temporaire_calcul_all_states import lire_all_states

    states = np.array(lire_all_states())
    cheat_dict, values = initialize_dict(states, game.pieces)

    nb_iter = 0

    while delta > epsilon * (1 - lamb) / 2 * lamb:
        nb_iter += 1
        delta = 0
        next_values: dict[tuple[State, Piece], float] = {}
        for state in states:
            for piece in game.pieces:
                next_gain, best_action = L(values, state, piece, game, lamb)
                delta = max(delta, abs(next_gain - values[(state, piece)]))

                next_values[(state, piece)] = next_gain
                cheat_dict[(state, piece)] = best_action

        values = next_values

        print(round(delta, 5))

    avg_gain = sum([values[key] for key in values.keys()]) / len(values)
    execution_time = round(time.time() - t1, 3)

    return (cheat_dict, avg_gain, round(delta, 5), execution_time, nb_iter)


def L(
    values: dict, state: State, piece: Piece, game, lamb: float
) -> tuple[float, PlayerAction]:
    """Bellman optimality equation"""
    max_gain = float("-inf")
    best_action = None

    for action in game.player_actions:
        next_state, reward, _ = game.next_state(
            state=state, action=action, incomming_piece=piece
        )

        expected_value = 0.0
        for next_piece in game.pieces:
            expected_value += values[(next_state, next_piece)]

        expected_value /= len(game.pieces)

        total_gain = reward + lamb * expected_value
        if total_gain > max_gain:
            max_gain = total_gain
            best_action = action

    return max_gain, best_action


def initialize_dict(states, pieces):

    values: dict[tuple[State, Piece], float] = {}
    for state in states:
        for piece in pieces:
            values[(state, piece)] = 0.0

    return {}, values


def save_cheat_dict():
    """Function to save the Value Iteration dict into Json filed"""
    cheat_dict, avg_gain, delta, execution_time, nb_iter = value_iteration(
        epsilon=0.1, lamb=0.99
    )

    serializable_dict = {
        json.dumps(
            {
                "state": state.to_tuple(),
                "piece": piece.to_tuple(),
            }
        ): action.to_dict()
        for (state, piece), action in cheat_dict.items()
    }

    with open("cheat_dict_lambda_0.99.json", "w") as fp:
        json.dump(serializable_dict, fp)

    print("avg_gain", avg_gain)
    print("delta", delta)
    print("execution time", execution_time)
    print("nb_iterations", nb_iter)
