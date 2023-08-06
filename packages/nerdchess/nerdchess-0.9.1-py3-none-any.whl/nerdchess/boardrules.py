"""Helps check for valid moves in the context of a board."""

from nerdchess import pieces
from nerdchess.move import Move


class BoardRules():
    """Applies different boardrules.

    Parameters:
        move: The boardmove to check against

    Attributes:
        move: The move we're checking
        valid: Is the checked move valid? see self.apply()
        origin: The origin square of the move
        destination: The destination square of the move
        piece: The piece being moved
    """

    def __init__(self, move, debug=False, check_checking=False):
        """Init."""
        self.move = move
        self.valid = True
        self.piece = self.move.origin_sq.occupant
        self.debug = debug
        self.check_checking = check_checking
        self.apply()

    def apply(self):
        """Apply boardrules based on the moved piece."""
        if isinstance(self.piece, pieces.Pawn):
            self.__pawn_rules()
        if not isinstance(self.piece, pieces.Knight):
            self.__blocking_pieces()
        if self.move.is_castling():
            if not self.check_checking:
                self.__castling()
        else:
            if self.move.is_capturing():
                self.__capturing()
            # self.__self_checking()

    def __capturing(self):
        """Check if this is a capturing move."""
        if (self.move.destination_sq.occupant.color ==
                self.move.origin_sq.occupant.color):
            self.valid = False

    def __pawn_rules(self):
        """Rules to apply to pawns only."""
        if (self.move.horizontal == 1
           or self.move.horizontal == -1):
            # If we're going horizontal, are we at least capturing?
            if not self.move.destination_sq.occupant:
                d_letter = self.move.destination[0]
                o_number = int(self.move.origin[1])
                # If not, is it at least en passant?
                pass_sq = self.move.board.squares[d_letter][o_number]
                if (isinstance(pass_sq.occupant, pieces.Pawn)
                   and pass_sq.occupant.color != self.piece.color):
                    self.enpassant = pass_sq
                else:
                    self.valid = False
        elif (self.move.vertical > 0
                or self.move.vertical < 0):
            if self.move.destination_sq.occupant:
                self.valid = False

    def __blocking_pieces(self):
        """Check if the move is being blocked."""
        for square in self.move.squares_between():
            if square.occupant:
                self.valid = False

    def __self_checking(self):
        """Check if the move puts the player itself in check."""
        newboard = self.move.board.new_board(self.move)
        if self.valid:
            if newboard.is_check(color=self.piece.color) == self.piece.color:
                self.valid = False

    def __castling(self):
        """Apply rules specific to castling."""
        pattern = []

        # TODO This introduces infinite recursion
        if self.move.board.is_check() == self.piece.color:
            self.valid = False

        if self.move.horizontal > 0:
            pattern = [
                (1, 0),
                (2, 0)
            ]
        else:
            pattern = [
                (-1, 0),
                (-2, 0)
            ]

        for move in pattern:
            inter_move = Move.from_position(self.piece.position, move)
            inter_board = self.move.board.new_board(inter_move)
            if inter_board.is_check() == self.piece.color:
                self.valid = False
