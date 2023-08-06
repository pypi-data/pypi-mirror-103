import pytest
from nerdchess import pieces
from nerdchess.config import colors
from nerdchess.move import Move


@pytest.fixture(scope='class', params=[
    pieces.Rook,
    pieces.Knight,
    pieces.Bishop,
    pieces.Queen,
    pieces.King
])
def piece(request):
    piece = request.param(colors.WHITE)
    piece.position = 'e4'
    return piece


class TestPieces():
    """Test some basic piece creation."""

    def test_creation(self, piece):
        assert isinstance(piece, pieces.Piece)

    def test_moves(self, piece):
        allowed_moves = piece.allowed_moves()

        assert isinstance(allowed_moves, list)
        for move in allowed_moves:
            assert isinstance(move, Move)

    def test_allowed_moves_board(self, piece, board_fixt):
        """Test the allowed moves in context of a board."""
        allowed_moves = piece.allowed_moves(board=board_fixt.board)

        assert isinstance(allowed_moves, list)
        for move in allowed_moves:
            assert isinstance(move, Move)
