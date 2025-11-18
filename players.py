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
        print("abscisse", action.abscisse) 
        #change of action until correct one is taken (no piece out of the grid by the right)
        while not(state.add_piece_is_valid(incomming_piece,action)):            
            print("Decision puts the piece out of the grid, random player is trying an other action \n")
            action = random.choice(actions)
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
