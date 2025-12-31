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

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))

    def to_str(self):
        # Convertit la forme en une chaîne valide pour ast.literal_eval
        shape_str = str(self.shape.tolist())
        return f"('{self.name}', {shape_str})"

    def to_tuple(self):
        return (
            self.name,
            tuple(map(tuple, self.shape.tolist())),
        )

    @classmethod
    def from_tuple(cls, t):
        name, shape = t
        return cls(name, np.array(shape))

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

    def to_dict(self):
        return {"nb_rotations": self.nb_rotations, "abscisse": self.abscisse}


@dataclass(frozen=True)
class SelectorAction:
    piece: Piece


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

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (
            self.nb_columns == other.nb_columns
            and self.height == other.height
            and np.array_equal(self.grid, other.grid)
        )

    def __hash__(self):
        return hash((self.nb_columns, self.height, self.grid.tobytes()))

    def to_tuple(self):
        """Converts a State into a tuple"""
        return tuple(tuple(1 if c else 0 for c in row) for row in self.grid.T)

    @classmethod
    def from_tuple(cls, grid):
        state = cls(len(grid[0]), len(grid))
        state.grid = np.array(grid, dtype=bool).T
        return state

    def to_str(self):
        grid_str = str(self.grid.tolist())
        return f"({self.nb_columns}, {self.height}, {grid_str})"

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

    def compute_nb_borders(self, incomming_piece: Piece, action: PlayerAction) -> int:
        """
        Count the number of borders with the incomming piece with a given action
        and the borders of the grid + other pieces
        """
        column = action.abscisse
        incomming_piece.rotate(nb_rotations=action.nb_rotations)

        line = 0
        while not self.collision_at(piece=incomming_piece, x=column, y=line):
            line += 1
        last_valid_abscisse = line - 1
        if last_valid_abscisse < 0:
            return 0  # loose

        nb_borders = 0

        for i in range(incomming_piece.height()):
            for j in range(incomming_piece.width()):
                if incomming_piece.shape[i, j]:
                    gx = column + j
                    gy = last_valid_abscisse + i

                    # borders with the grid
                    if gx == 0 or gx == self.nb_columns - 1:
                        nb_borders += 1
                    if gy == self.height - 1:
                        nb_borders += 1

                    # borders with other pieces
                    if gx + 1 < self.nb_columns and not self.grid[gx + 1, gy]:
                        nb_borders += 1
                    if gx - 1 >= 0 and not self.grid[gx - 1, gy]:
                        nb_borders += 1
                    if gy + 1 < self.height and not self.grid[gx, gy + 1]:
                        nb_borders += 1

        return nb_borders

    def add_piece_is_valid(self, piece: Piece, action: PlayerAction) -> bool:
        "Tells if the action is allowed (piece doesn't go outside on the right)"
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
