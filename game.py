import numpy as np
from state import Piece, PlayerAction, SelectorAction, State
from players import Selector, Player


class Game:
    """Represents a session of the Tetris game"""

    def __init__(self, nb_colums: int, height: int, player: Player, selector: Selector):
        self.player = player
        self.selector = selector
        self.state = State(nb_columns=nb_colums, height=height)
        self.pieces: list[Piece] = [
            Piece(name="line", shape=np.array([[1, 1, 1]])),
            Piece(name="square", shape=np.array([[1, 1], [1, 0]])),
        ]
        self.initialize_actions()

    def initialize_actions(self):
        self.player_actions: list[PlayerAction] = []

        # no rotation
        for n in range(self.state.nb_columns):
            self.player_actions.append(PlayerAction(nb_rotations=0, abscisse=n))

        # 90 rotation
        for n in range(self.state.nb_columns):
            self.player_actions.append(PlayerAction(nb_rotations=1, abscisse=n))

        # 180 rotation
        for n in range(self.state.nb_columns):
            self.player_actions.append(PlayerAction(nb_rotations=2, abscisse=n))

        # 270 rotation
        for n in range(self.state.nb_columns):
            self.player_actions.append(PlayerAction(nb_rotations=3, abscisse=n))

        self.selector_actions: list[SelectorAction] = [
            SelectorAction(piece=self.pieces[0]),
            SelectorAction(piece=self.pieces[1]),
        ]

    def play(self, visualisation=False):
        """Main logic about a tetris game"""
        game_can_continue = True
        player_r = 0
        iter = 0
        iterations = []
        scores = []

        while game_can_continue:
            iter += 1

            selector_action = self.selector.choose_strategy(
                state=self.state, actions=self.selector_actions
            )
            incomming_piece = selector_action.piece

            if visualisation:
                print("incomming piece")
                print(incomming_piece)
                print(self.state)
                print("Actual player score = ", player_r)
                print("\n")

            player_action = self.player.choose_strategy(
                incomming_piece=incomming_piece,
                state=self.state,
                actions=self.player_actions,
            )

            self.state, p_r, selector_r = self.next_state(
                state=self.state,
                action=player_action,
                incomming_piece=incomming_piece,
            )
            player_r += p_r

            if selector_r == 1:
                game_can_continue = False
                if visualisation:
                    print("Player score", player_r)
                    print("LOOOOOOOOOOOSE")

            scores.append(player_r)
            iterations.append(iter)

            if iter >= 10000:
                if visualisation:
                    print("INFINITE GAIN: stopped at 10000 iterations")
                    # break
                return iterations, scores
        return iterations, scores

    def next_state(self, state: State, action: PlayerAction, incomming_piece: Piece):
        """Return a new state without changing the main one and compute assiociated rewards"""
        new_state: State = state.copy()
        piece_added = new_state.add_piece(piece=incomming_piece.copy(), action=action)

        player_r, selector_r = self.reward(piece_added=piece_added, state=new_state)

        return new_state, player_r, selector_r

    def reward(self, piece_added: bool, state: State) -> tuple[int, int]:
        """Return player's reward, selector's reward"""
        if not piece_added:
            return (-1, 1)  # selector won

        nb_full_lines = state.count_number_full_lines()

        if nb_full_lines == 0:
            return (0, 0)

        if nb_full_lines == 1:
            return (1, 0)

        if nb_full_lines == 2:
            return (3, 0)

        if nb_full_lines == 3:
            return (6, 0)
