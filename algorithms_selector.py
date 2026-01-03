from copy import deepcopy
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

import time

import numpy as np

from state import Piece, PlayerAction, State
from players import RandomPlayer, Randomselector, ValueIterationPlayer


def save_reverse_cheatdict(epsilon, lambd, indicator, type=True):
    """Save the reverse cheatdict for the selector from the VI in
    the file 'reverse_cheatdict/reverse_cheatdict_epsilon_lambd'

    indicator = True will give a result according to random player

    type = True gives a VI with a 0/1 reward
    type = False saves a VI with a 0,-1,-3,-6 reward
    """
    reverse_cheatdict = value_iteration_selector(
        epsilon, lambd, type=type, indicator=indicator
    )

    serializable_dict = {
        json.dumps({"state": state.to_tuple()}): piece.to_tuple()
        for state, piece in reverse_cheatdict.items()
    }
    if type:
        if indicator:
            txt = f"reverse_cheatdict/reverse_cheatdict_random_{str(epsilon)}_{str(lambd)}"
        else:
            txt = f"reverse_cheatdict/reverse_cheatdict_VI_{str(epsilon)}_{str(lambd)}"
    else:
        txt = f"reverse_cheatdict_reward2/reverse_cheatdict_random_{str(epsilon)}_{str(lambd)}"
    with open(txt, "w") as f:
        data = json.dump(serializable_dict, f)
        if not (type):
            print(
                f"CHARGEMENT DONE VI SELECTOR on random player with opposite negative reward and epsilon = {epsilon} et lambda = {lambd}"
            )
        else:
            print(
                f"CHARGEMENT DONE VI SELECTOR (Random : {indicator}) epsilon = {epsilon} et lambda = {lambd}"
            )


def value_iteration_selector(epsilon: float, lambd: float, type: bool, indicator=True):
    """Returns a dictionnary dict[State] = Piece : from a special state give the worse
    possible piece to the player
    indicator = True : Random player used to calculate in the process of Bellman"""
    from fichier_temporaire_calcul_all_states import lire_all_states
    from game import Game

    play = ValueIterationPlayer(f"cheatdict/cheat_dict_lambda_0.5.json")
    game = Game(4, 4, play, Randomselector())
    all_states = lire_all_states()
    V0 = {state: 0 for state in all_states}
    d0 = {}
    count = 0
    delta = float("inf")
    while delta > epsilon * (1 - lambd) / (2 * lambd):
        newV = {}
        newD = {}
        for state in all_states:
            if indicator:
                max_gain, best_piece = L_random(state, V0, lambd, type=type)
            else:
                game.state = state
                max_gain, best_piece = L(state, V0, lambd, game)
            newV[state] = max_gain
            newD[state] = best_piece
        delta = N_8(V0, newV)
        d0 = newD
        V0 = newV
        count += 1
        print(count)
        print(f"delta = {delta}")

    return d0


def L_random(state: State, V: dict[State], lambd: float, type: bool):
    """Returns the maximum gain and the associated best choice of piece from state given
    V is the actual expected gain used in Bellman optimality equation
    A random player is used during the calculation"""
    from game import Game

    game = Game(4, 4, RandomPlayer(), Randomselector())
    game.state = state
    total = {p: 0 for p in game.pieces}
    for p in game.pieces:
        piece = p.copy()
        total[p] = rewardSelector(state=state, piece=piece, type=type)
        somme = 0
        for action in game.player_actions:
            new_state: State = state.copy()
            piece = p.copy()
            if new_state.add_piece(piece, action):
                new_state: State = state.copy()
                piece = p.copy()
                next_state, _, _ = game.next_state(new_state, action, piece)
                somme += V[next_state]
            else:
                pass
        total[p] += lambd * somme
    if total[game.pieces[0]] > total[game.pieces[1]]:
        return total[game.pieces[0]] / len(game.player_actions), game.pieces[0]
    else:
        return total[game.pieces[1]] / len(game.player_actions), game.pieces[1]


def rewardSelector(state: State, piece: Piece, type: bool):
    """
    Gives the reward of the selector from a state and a piece chosen for the value iteration

    Type = True <-> reward = 1 / 0
    Type = False <-> reward = - (average reward_player) (hence with (0,-1,-3,-6))
    """
    from game import Game

    game = Game(4, 4, RandomPlayer(), Randomselector())
    if type:
        total = 0
        for action in game.player_actions:
            new_state: State = state.copy()
            new_piece = piece.copy()
            if not (new_state.add_piece(new_piece, action)):
                total = 1
                break
        return total
    else:
        mean = 0
        for action in game.player_actions:
            new_state = state.copy()
            game.state = new_state
            new_piece = piece.copy()
            if new_state.add_piece(new_piece, action):
                new_state, player_r, _ = game.next_state(
                    state=state, action=action, incomming_piece=new_piece
                )
                mean -= player_r
        return mean / len(game.player_actions)


def L(state: State, V: dict[State], lambd: float, game):
    """Computes the max gain and best choic of piece for the selector when facing the
    value iteration player"""
    game.state = state
    total = {p: 0 for p in game.pieces}
    for p in game.pieces:
        piece = p.copy()
        new_state = state.copy()
        play = game.player
        action = play.choose_strategy(piece, state, game.player_actions)
        if new_state.add_piece(piece, action):
            piece = p.copy()
            game.state, _, _ = game.next_state(state, action, piece)
            total[p] = lambd * V[state]
        else:
            total[p] = 1
    if total[game.pieces[0]] > total[game.pieces[1]]:
        return total[game.pieces[0]], game.pieces[0]
    else:
        return total[game.pieces[1]], game.pieces[1]


def N_8(V1, V2):
    """Renvoie norme infinie du vecteur V1-V2"""
    rst = 0
    for elt in V1.keys():
        if abs(V1[elt] - V2[elt]) > rst:
            rst = abs(V1[elt] - V2[elt])
        else:
            pass
    return rst


# saving of VI selector on random player & reward 0/1
save_reverse_cheatdict(0.001, 0.1, indicator=True, type=True)
save_reverse_cheatdict(0.001, 0.5, indicator=True, type=True)
save_reverse_cheatdict(0.001, 0.9, indicator=True, type=True)

# saving of VI selector on VI player & reward 0/1
save_reverse_cheatdict(0.001, 0.1, indicator=False, type=True)
save_reverse_cheatdict(0.001, 0.5, indicator=False, type=True)
save_reverse_cheatdict(0.001, 0.9, indicator=False, type=True)

# saving of VI selector on random player & reward 0,-1,-3,-6
save_reverse_cheatdict(0.001, 0.1, indicator=False, type=False)
save_reverse_cheatdict(0.001, 0.5, indicator=False, type=False)
save_reverse_cheatdict(0.001, 0.9, indicator=False, type=False)


def infos_reverse_cheatdict(filename):
    """Gives the reverse cheatdict requested, and its size"""
    with open(filename, "r") as f:
        data = json.load(f)
    print(data)
    print(len(data))


# infos_reverse_cheatdict("reverse_cheatdict/reverse_cheatdict_0.1_0.1")
