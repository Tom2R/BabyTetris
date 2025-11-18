from copy import deepcopy
from dataclasses import dataclass
import numpy as np


class Piece:
    """
    Examples of pieces:

    [[1,1,1]] is the line

    [[1, 1],
     [1, 0]] is an angle
    """

    def __init__(self, name: str, shape: np.ndarray):
        self.name = name
        self.shape = shape

    def __repr__(self):
        rows = []
        for i in range(self.height()):
            row = []
            for j in range(self.width()):
                row.append("#" if self.shape[i, j] else ".")
            rows.append(" ".join(row))
        return "\n".join(rows)

    def copy(self):
        """Return a new identical piece"""
        return Piece(name=self.name, shape=deepcopy(self.shape))

    def width(self):
        """return width's piece"""
        return self.shape.shape[1]

    def height(self):
        """Return height's piece"""
        return self.shape.shape[0]

    def rotate(self, nb_rotations: int = 1, clockwise: bool = True) -> None:
        """
        Rotate the piece by 90° * nb_rotations.
        clockwise=True -> rotate clockwise
        """
        if nb_rotations % 4 == 0:
            return
        k = nb_rotations % 4
        if clockwise:
            k = -k  # clockwise -> negative k
        self.shape = np.rot90(self.shape, k=k)


class PlayerAction:
    def __init__(self, nb_rotations: int, abscisse: int):
        self.nb_rotations = nb_rotations
        self.abscisse = abscisse


@dataclass(frozen=True)
class SelectorAction:
    piece: Piece


class Transition:
    """Transition matrix"""

    def __init__(self):
        pass


class State:
    def __init__(self, nb_columns: int, height: int, grid=False):
        """
        Specific moment of the game
        we have a matrix, with True if the space is free in (x,y), false overwise"""
        self.nb_columns = nb_columns
        self.height = height

        if grid is False:
            self.grid = np.ones((self.nb_columns, self.height), dtype=bool)


        else:
            self.grid = grid


    def __repr__(self):

        rows = []
        for y in range(self.height):
            row = []
            for x in range(self.nb_columns):
                if self.grid[x, y]:
                    row.append(".")  # free
                else:
                    row.append("#")  # occupied
            rows.append(" ".join(row))
        return "\n".join(rows)



    def copy(self):
        """Return a new identical state"""
        return State(
            nb_columns=self.nb_columns, height=self.height, grid=deepcopy(self.grid)
        )

    def collision_at(self, piece: Piece, x: int, y: int) -> bool:
        """
        Return True if you have a collision placing the piece in (x,y).
        Important: (x,y) represents the hight left point of the piece
        """
        # if y == self.height - 1:
        #    breakpoint()
        for i in range(piece.height()):
            for j in range(piece.width()):
                if piece.shape[i, j]:
                    gx = x + j
                    gy = y + i

                    # Out of grid
                    if gx < 0 or gx >= self.nb_columns or gy < 0 or gy >= self.height:
                        return True

                    # already occupied cell
                    if not self.grid[gx, gy]:
                        return True

        return False

    def add_piece(self, piece: Piece, action: PlayerAction) -> bool:
        """Add the piece to the grid, if you can't return False"""

        column = action.abscisse
        piece.rotate(nb_rotations=action.nb_rotations)

        print("piece after rotations")
        print(piece)
        print("abscisse", column)

        line = 0
        while not self.collision_at(piece=piece, x=column, y=line):
            line += 1

        last_valid_abscisse = line - 1

        if last_valid_abscisse < 0:
            return False  # loose game

        for i in range(piece.height()):
            for j in range(piece.width()):
                if piece.shape[i, j]:
                    self.grid[column + j, last_valid_abscisse + i] = False

        return True
  
    def add_piece_is_valid(self,piece: Piece, action: PlayerAction) -> bool:
        "Tells if the action is allowed (piece doesn't go outside on the right) "
        piece_chosen = piece.copy()
        piece_chosen.rotate(action.nb_rotations)
        if action.abscisse + piece_chosen.width() - 1 >= self.nb_columns:
            return False
        else:
            return True
        
    def count_number_full_lines(self) -> int:
        """Count the number of full lines and update the grid"""
        nb_full_lines = 0
        new_grid = np.ones_like(self.grid, dtype=bool)

        # we start from the bottom of the grid and we go up
        write_line = self.height - 1
        for y in range(self.height - 1, -1, -1):
            is_full = all(not self.grid[x, y] for x in range(self.nb_columns))
            if is_full:
                nb_full_lines += 1
            else:
                for x in range(self.nb_columns):
                    new_grid[x, write_line] = self.grid[x, y]
                write_line -= 1

        self.grid = new_grid

        return nb_full_lines
