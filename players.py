from abc import ABC, abstractmethod
import json
import random

import numpy as np


from state import PlayerAction, SelectorAction, State, Piece


class Player(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def choose_strategy(
        self, incomming_piece: Piece, state: State, actions: list[PlayerAction]
    ) -> PlayerAction:
        "player should always have a strategy"
        pass


class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def choose_strategy(
        self, incomming_piece: Piece, state: State, actions: list[PlayerAction]
    ):
        """Player plays randomly"""
        action = random.choice(actions)

        # change of action until correct one is taken (no piece out of the grid by the right)
        while not (state.add_piece_is_valid(incomming_piece, action)):
            print(
                "Decision puts the piece out of the grid, random player is trying an other action \n"
            )
            action = random.choice(actions)
        return action


class ValueIterationPlayer(Player):
    def __init__(self, cheatdict_name: str):
        super().__init__()
        self.cheat_dict = self.load_cheat_dict(cheatdict_name)

    def load_cheat_dict(self, filename):
        with open(filename, "r") as fp:
            loaded = json.load(fp)

        cheat_dict = {}

        for key_json, action_dict in loaded.items():
            data = json.loads(key_json)

            state = State.from_tuple(data["state"])
            piece = Piece.from_tuple(data["piece"])
            action = PlayerAction(**action_dict)

            cheat_dict[(state, piece)] = action

        return cheat_dict

    def choose_strategy(
        self, incomming_piece: Piece, state: State, actions: list[PlayerAction]
    ):
        """Player follows the cheat dict"""

        action = self.cheat_dict[(state, incomming_piece)]

        return action


class CompactPlayer(Player):
    """
    Player who places the incoming piece in the most compact way possible
    (the place with the most shared borders with pieces on the grid).
    """

    def __init__(self):
        pass

    def get_action_with_better_compactness(
        self, incomming_piece: Piece, state: State, actions: list[PlayerAction]
    ) -> PlayerAction:
        """Place the piece in the most compact spot on the grid."""
        most_borders = 0
        for action in actions:
            nb_borders = state.compute_nb_borders(incomming_piece.copy(), action)
            if nb_borders >= most_borders:
                most_borders = nb_borders
                best_action = action
        return best_action

    def choose_strategy(self, incomming_piece, state, actions) -> PlayerAction:
        """Plays with compact strategy"""
        return self.get_action_with_better_compactness(incomming_piece, state, actions)


class LineEliminator(CompactPlayer):
    """
    player who plays the action that eliminates a line if possible and plays compactly otherwise
    """

    def __init__(self):
        super().__init__()

    def choose_strategy(self, incomming_piece, state, actions) -> PlayerAction:

        # first: see if you can eliminate a line
        for action in actions:
            new_state: State = state.copy()
            piece_added = new_state.add_piece(
                piece=incomming_piece.copy(), action=action
            )
            if piece_added:
                nb_full_lines = new_state.count_number_full_lines()

                if nb_full_lines >= 1:
                    return action

        # Second: play in compact strategy if you can not eliminate line
        return self.get_action_with_better_compactness(incomming_piece, state, actions)


class RobustPlayer(CompactPlayer):
    """
    I choose an action such that if I have the worst piece next, I can still make an interesting move (remove a row or compact).

    """

    def __init__(self):
        super().__init__()
        self.possible_pieces: list[Piece] = [
            Piece(name="line", shape=np.array([[1, 1, 1]])),
            Piece(name="square", shape=np.array([[1, 1], [1, 0]])),
        ]

    def best_future_score(
        self, state: State, piece: Piece, actions: list[PlayerAction]
    ) -> int:
        """
        Best score for a given future piece.
        We suppose that we will play smartely in the future.
        """
        best = -1
        for action in actions:
            if not state.add_piece_is_valid(piece, action):
                continue

            new_state = state.copy()
            if not new_state.add_piece(piece.copy(), action):
                continue

            full_lines = new_state.count_number_full_lines()
            compactness = state.compute_nb_borders(piece.copy(), action)

            best = max(best, compactness + 100 * full_lines)

        return best

    def choose_strategy(
        self, incomming_piece: Piece, state: State, actions: list[PlayerAction]
    ) -> PlayerAction:
        """
        We try to find the action that maximizes the score of the future move in the worst scenario (annoying piece)
        MAX in the actions of (MIN in the pieces(score))
        """

        best_score = -1
        best_action = None

        for action in actions:
            if not state.add_piece_is_valid(incomming_piece, action):
                continue

            new_state = state.copy()
            if not new_state.add_piece(incomming_piece.copy(), action):
                continue

            # Pessimistic with the next piece
            worst_case_score = min(
                self.best_future_score(new_state, futur_piece, actions)
                for futur_piece in self.possible_pieces
            )

            if worst_case_score >= best_score:
                best_score = worst_case_score
                best_action = action

        if best_action is None:
            return self.get_action_with_better_compactness(
                incomming_piece, state, actions
            )

        return best_action


class Selector(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def choose_strategy(
        self, state: State, actions: list[SelectorAction]
    ) -> SelectorAction:
        """A selector should always have a method that chooses a strategy"""
        pass


class Randomselector(Selector):
    def __init__(self):
        super().__init__()

    def choose_strategy(self, state: State, actions: list[SelectorAction]):
        """Random piece selection"""
        return random.choice(actions)


class GreedySelector(Selector):
    """
    Selector qui donne une pièce minimisant le maximum des scores
    pouvant être obtenus par le joueur
    """

    def __init__(self):
        super().__init__()

    def choose_strategy(self, state: State, actions: list[SelectorAction]):

        pieces: list[Piece] = [
            Piece(name="line", shape=np.array([[1, 1, 1]])),
            Piece(name="square", shape=np.array([[1, 1], [1, 0]])),
        ]
        player_actions: list[PlayerAction] = []

        # no rotation
        for n in range(4):
            player_actions.append(PlayerAction(nb_rotations=0, abscisse=n))

        # 90 rotation
        for n in range(4):
            player_actions.append(PlayerAction(nb_rotations=1, abscisse=n))

        # 180 rotation
        for n in range(4):
            player_actions.append(PlayerAction(nb_rotations=2, abscisse=n))

        # 270 rotation
        for n in range(4):
            player_actions.append(PlayerAction(nb_rotations=3, abscisse=n))

        minimum = 6
        best_piece = None
        total = {p: 0 for p in pieces}
        for p in pieces:
            reward_max = 0
            for action in player_actions:
                new_state = state.copy()
                piece = p.copy()
                if new_state.add_piece_is_valid(piece, action):
                    if new_state.add_piece(piece, action):
                        nb_full_lines = new_state.count_number_full_lines()
                        if new_state.score(nb_full_lines=nb_full_lines) > reward_max:
                            reward_max = new_state.score(nb_full_lines=nb_full_lines)

            total[p] = reward_max
            # if reward_max < minimum:
            #     best_piece = p
            #     minimum = reward_max

        if total[pieces[0]] == total[pieces[1]]:
            best_piece = random.choice(actions).piece
        elif total[pieces[0]] > total[pieces[1]]:
            best_piece = pieces[1]
        else:
            best_piece = pieces[0]

        if best_piece == None:
            best_piece = random.choice(actions)
        return SelectorAction(best_piece)


class ValueIterationSelector(Selector):
    def __init__(self, vi_player: bool, epsilon: float, lambd: float, type: bool):
        """
        If type we use the selector trained with VI with negative reward

        Else
        {
        if vi_player we use the selector trained with VI with 0/1 reward and a vi_player

        if not(vi_player) we use the selector trained with VI with random player
        }

        """
        super().__init__()
        if type:
            reverse_cheatdict_name = (
                f"reverse_cheatdict_reward2/reverse_cheatdict_random_{epsilon}_{lambd}"
            )
            self.reverse_cheat_dict = self.load_reverse_cheat_dict(
                reverse_cheatdict_name
            )
        else:
            if vi_player:
                reverse_cheatdict_name = (
                    f"reverse_cheatdict/reverse_cheatdict_VI_{epsilon}_{lambd}"
                )
            else:
                reverse_cheatdict_name = (
                    f"reverse_cheatdict/reverse_cheatdict_random_{epsilon}_{lambd}"
                )
            self.reverse_cheat_dict = self.load_reverse_cheat_dict(
                reverse_cheatdict_name
            )

    def load_reverse_cheat_dict(self, filename):
        with open(filename, "r") as fp:
            loaded = json.load(fp)

        reverse_cheat_dict = {}

        for key_json, piece_chosen in loaded.items():
            data = json.loads(key_json)

            state = State.from_tuple(data["state"])
            piece_action = Piece.from_tuple(piece_chosen)

            reverse_cheat_dict[state] = piece_action

        return reverse_cheat_dict

    def choose_strategy(self, state: State, actions: list[SelectorAction]):
        """Selector follows piece selection dico with the actual state"""
        return SelectorAction(self.reverse_cheat_dict[state])
