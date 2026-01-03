from players import (
    Player,
    ValueIterationPlayer,
    RandomPlayer,
    RobustPlayer,
    LineEliminator,
    CompactPlayer,
    HoleFillerPlayer,
    Selector,
    Randomselector,
    GreedySelector,
    ValueIterationSelector,
)
from game import Game
import time


def launch_war():
    deterministic_players: dict[str, Player] = {
        "VI_0.1": ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.1.json"
        ),
        "VI_0.5": ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.5.json"
        ),
        "VI_0.9": ValueIterationPlayer(
            cheatdict_name="cheatdict/cheat_dict_lambda_0.9.json"
        ),
        "Robust": RobustPlayer(),
        "lineEliminator": LineEliminator(),
        "Compact": CompactPlayer(),
        "Hole": HoleFillerPlayer(),
    }
    randomized_players: dict[str, Player] = {
        "Random": RandomPlayer(),
    }

    deterministic_selectors: dict[str, Selector] = {
        "VI_in_VI_player_O/1_reward_0.1": ValueIterationSelector(
            vi_player=True, epsilon=0.001, lambd=0.1, type=False
        ),
        "VI_in_VI_player_O/1_reward_0.5": ValueIterationSelector(
            vi_player=True, epsilon=0.001, lambd=0.5, type=False
        ),
        "VI_in_VI_player_O/1_reward_O.9": ValueIterationSelector(
            vi_player=True, epsilon=0.001, lambd=0.9, type=False
        ),
        "VI_in_random_player_O/1_reward_0.1": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.1, type=False
        ),
        "VI_in_random_player_O/1_reward_0.5": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.5, type=False
        ),
        "VI_in_random_player_O/1_reward_O.9": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.9, type=False
        ),
        "VI_in_random_player_reverse_reward_0.1": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.1, type=True
        ),
        "VI_in_random_player_reverse_reward_0.5": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.5, type=True
        ),
        "VI_in_random_player_reverse_reward_O.9": ValueIterationSelector(
            vi_player=False, epsilon=0.001, lambd=0.9, type=True
        ),
    }
    randomized_selectors: dict[str, Selector] = {
        "random": Randomselector(),
        "greedy": GreedySelector(),
    }
    pass
