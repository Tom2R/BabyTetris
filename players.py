from abc import ABC, abstractmethod
import random

from game import Piece
from state import PlayerAction, SelectorAction, State


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
        print(incomming_piece)
        print("nb_rotations", action.nb_rotations)

        # Change the abscisse if the piece is out of the grid by the right
        if incomming_piece.width() == 2 and action.abscisse >= state.nb_columns - 2:
            action.abscisse -= 1
            return action

        if incomming_piece.name == "line" and action.nb_rotations % 2 == 0:
            if action.abscisse == state.nb_columns - 2:
                print(action.abscisse)
                action.abscisse -= 1
                return action
            if action.abscisse == state.nb_columns - 1:
                print(action.abscisse)
                print(incomming_piece)
                action.abscisse -= 2

                return action

        return action


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
