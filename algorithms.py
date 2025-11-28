from copy import deepcopy
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import time

import numpy as np

from state import Piece, PlayerAction, State


def value_iteration(epsilon: float = 0.7, lamb: float = 0.8) -> dict:
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

    while delta > epsilon * (1 - lamb) / 2 * lamb:
        delta = 0
        next_values: dict[tuple[State, Piece], float] = {}
        for state in states:
            for piece in game.pieces:
                next_gain, best_action = L(values, state, piece, game, lamb)
                delta = max(delta, abs(next_gain - values[(state, piece)]))

                next_values[(state, piece)] = next_gain
                cheat_dict[(state, piece)] = best_action
        values = next_values
        sum = 0
        for key in values.keys():
            sum += values[key]
        print(sum/len(values))
        print(round(delta, 3))

    print("execution_time", round(time.time() - t1, 1))

    return cheat_dict,0.5*values[(State(4,4),game.pieces[0])]+0.5*values[(State(4,4),game.pieces[1])]


def L(
    values: dict, state: State, piece: Piece, game, lamb: float
) -> tuple[float, PlayerAction]:
    """Bellman optimality equation"""
    max_gain = float("-inf")
    best_action = None
    copied_piece = piece.copy()
    for action in game.player_actions:
        next_state, reward, _ = game.next_state(
            state=state, action=action, incomming_piece=copied_piece
        )

        expected_value = 0.0
        for next_piece in game.pieces:
            expected_value += values[(next_state, next_piece)]

        expected_value /= len(game.pieces)

        total_gain = reward + lamb * expected_value
        if total_gain > max_gain:
            max_gain = total_gain
            best_action = action
    #breakpoint()

    return max_gain, best_action


def initialize_dict(states, pieces):

    values: dict[tuple[State, Piece], float] = {}
    for state in states:
        for piece in pieces:
            values[(state, piece)] = 0.0

    return {}, values


def policy_iteration():
    pass

