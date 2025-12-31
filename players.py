from abc import ABC, abstractmethod
import json
import random


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

    def choose_strategy(self, incomming_piece, state, actions) -> PlayerAction:
        """Place the piece in the most compact spot on the grid."""
        most_borders = 0
        for action in actions:
            nb_borders = state.compute_nb_borders(incomming_piece.copy(), action)
            if nb_borders >= most_borders:
                most_borders = nb_borders
                best_action = action
        return best_action


class LineEliminator(Player):
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
        most_borders = 0
        for action in actions:
            nb_borders = state.compute_nb_borders(incomming_piece.copy(), action)
            if nb_borders >= most_borders:
                most_borders = nb_borders
                best_action = action
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


class ValueIterationOnRandomSelector(Selector):
    def __init__(self, reverse_cheatdict_name: str):
        super().__init__()
        self.reverse_cheat_dict = self.load_reverse_cheat_dict(reverse_cheatdict_name)

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
