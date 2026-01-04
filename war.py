import numpy as np
import pandas as pd
from copy import deepcopy
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
    MultiArmedSelector,
)
from game import Game
import time


def launch_war(nb_samples_random=1):
    start_time = time.time()
    deterministic_players: dict[str, Player] = {
        "VI_0.1": ValueIterationPlayer("cheatdict/cheat_dict_lambda_0.1.json"),
        "VI_0.5": ValueIterationPlayer("cheatdict/cheat_dict_lambda_0.5.json"),
        "VI_0.9": ValueIterationPlayer("cheatdict/cheat_dict_lambda_0.9.json"),
        "Robust": RobustPlayer(),
        "lineEliminator": LineEliminator(),
        "Compact": CompactPlayer(),
        "Hole": HoleFillerPlayer(),
    }

    randomized_players: dict[str, Player] = {
        "Random": RandomPlayer(),
    }

    deterministic_selectors: dict[str, Selector] = {
        "VI_in_VI_O/1_0.1": ValueIterationSelector(True, 0.001, 0.1, True),
        "VI_in_VI_O/1_0.5": ValueIterationSelector(True, 0.001, 0.5, True),
        "VI_in_VI_O/1_O.9": ValueIterationSelector(True, 0.001, 0.9, True),
        "VI_in_random_O/1_0.1": ValueIterationSelector(False, 0.001, 0.1, True),
        "VI_in_random_O/1_0.5": ValueIterationSelector(False, 0.001, 0.5, True),
        "VI_in_random_O/1_O.9": ValueIterationSelector(False, 0.001, 0.9, True),
        "VI_in_random_reverse_0.1": ValueIterationSelector(False, 0.001, 0.1, False),
        "VI_in_random_reverse_0.5": ValueIterationSelector(False, 0.001, 0.5, False),
        "VI_in_random_reverse_O.9": ValueIterationSelector(False, 0.001, 0.9, False),
    }

    randomized_selectors: dict[str, Selector] = {
        "random": Randomselector(),
        "greedy": GreedySelector(),
    }

    all_players = list(deterministic_players.keys()) + list(randomized_players.keys())
    all_selectors = list(deterministic_selectors.keys()) + list(
        randomized_selectors.keys()
    )

    final_score_df = pd.DataFrame(index=all_selectors, columns=all_players)
    slope_df = pd.DataFrame(index=all_selectors, columns=all_players)

    for player_name, player in {**deterministic_players, **randomized_players}.items():
        for selector_name, selector in {
            **deterministic_selectors,
            **randomized_selectors,
        }.items():
            print("NEW BATTLE")
            if (player_name in deterministic_players) and (
                selector_name in deterministic_selectors
            ):
                samples = 1
            else:
                samples = nb_samples_random

            scores, slopes = run_game(player, selector, samples)

            final_score_df.loc[selector_name, player_name] = (
                f"{np.mean(scores):.1f} ± {np.std(scores):.1f}"
            )
            slope_df.loc[selector_name, player_name] = (
                f"{np.mean(slopes):.2f} ± {np.std(slopes):.2f}"
            )

    print("FINAL SCORES (mean ± std)")
    print(final_score_df)
    print("\n SLOPES (mean ± std)")
    print(slope_df)

    with pd.ExcelWriter("resultats_simulation.xlsx") as writer:
        final_score_df.to_excel(writer, sheet_name="Scores")
        slope_df.to_excel(writer, sheet_name="Slopes")

    print("execution time", round((time.time() - start_time) / 60))


def run_game(player: Player, selector: Selector, samples=1):
    scores_all = []
    slopes_all = []
    for _ in range(samples):
        game = Game(
            nb_colums=4,
            height=4,
            player=deepcopy(player),
            selector=deepcopy(selector),
        )
        iterations, scores = game.play(visualisation=False)
        final_score = scores[-1]
        slope = final_score / len(iterations)
        scores_all.append(final_score)
        slopes_all.append(slope)
    return scores_all, slopes_all


launch_war()
