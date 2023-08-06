"""Start a game of chess.

This module offers a simple interface to start a game of chess.
The game consists of:
    - 2 Players
    - A board
    - Pieces
    - Pawns

Example:
    chessgame = game.ChessGame(player_1, player_2)
"""

from nerdchess import pieces
from nerdchess import game_event
from nerdchess.config import colors
from nerdchess.board import Board
from nerdchess.boardmove import BoardMove


class ChessGame():
    """Creates a new chessgame with players, pieces, and sets up the board.

    Main interface for nerdchess.
    Args and returns for public functions should inherit the GameEvent type.

    Parameters:
        name_1(Player): Player 1
        name_2(Player): Player 2
        over(Bool): Whether the game is over

    Attributes:
        player_1(Player): Player 1
        player_2(Player): Player 2
        playerlist(list): A list of the two players
        board(Board): The board the game is played on
        pieces(list): A list of the pieces the game is played with
        pawns(list): A list of the pawns the game is played with
    """

    def __init__(self, player_1, player_2, over=False):
        """Init."""
        self.player_1 = player_1
        self.player_2 = player_2
        self.playerlist = [self.player_1, self.player_2]

        self.board = Board()
        self.pieces = pieces.create_pieces()
        self.pawns = pieces.create_pawns()
        self.board.setup_board(self.pieces, self.pawns)

        self.board_history = []

        self.over = over

    def pass_turn(self):
        """Pass the turn to the other player."""
        for player in self.playerlist:
            player.turn = False if player.turn else True

    def move(self, player, move):
        """Process the move in a game of chess.

        Parameters:
            player: The player that made the move
            move: The move representeed by squares (eg. e2e4)

        Returns:
            Bool: Was the move succesful?
        """
        move = BoardMove(self.board, move)

        if not player.turn:
            return game_event.MoveEvent(False)

        if move.origin_sq.occupant:
            if move.origin_sq.occupant.color != player.color:
                return game_event.MoveEvent(False)
        else:
            return game_event.MoveEvent(False)

        result = move.process()
        if result:
            self.board_history.append(self.board)
            if result.is_checkmate():
                self.over = True
            self.board = result
            self.pass_turn()
            return game_event.MoveEvent(True, promotion=move.promotion)
        else:
            return game_event.MoveEvent(False)

    def promote(self, pawn, target):
        """Promote a pawn.

        Parameters:
            pawn: The pawn object to promote
            target: The target nerdchess.Piece object

        returns:
            PromotionEvent: Result object containing event information
        """
        if not isinstance(pawn, pieces.Pawn):
            return game_event.PromotionEvent(False)

        if pawn.color == colors.WHITE:
            if pawn.last_move.text[3] == '8':
                return game_event.MoveEvent(self.board.promote(pawn, target))
            else:
                return game_event.MoveEvent(False)
        else:
            if pawn.last_move.text[3] == '1':
                return game_event.MoveEvent(self.board.promote(pawn, target))
            else:
                return game_event.MoveEvent(False)

