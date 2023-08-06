import pytest
from types import SimpleNamespace
from nerdchess.board import Board
from nerdchess.boardmove import BoardMove
from nerdchess import pieces
from nerdchess.config import colors


@pytest.fixture
def board_queen_e4(board_fixt):
    """ Empty board with queen on e4. """
    board_fixt.place_piece(pieces.Queen(colors.WHITE), 'e4')
    return board_fixt.board


class TestDirections():
    """ Test directional movement with a queen on e4. """

    def test_diagonal(self, board_queen_e4):
        move = BoardMove(board_queen_e4, 'e4c2')
        result = move.process()

        assert move.square_selectors_between() == ['d3']
        assert result

    def test_horizontal(self, board_queen_e4):
        move = BoardMove(board_queen_e4, 'e4a4')
        result = move.process()

        assert move.square_selectors_between() == [
            'd4', 'c4', 'b4'
        ]
        assert result

    def test_vertical(self, board_queen_e4):
        move = BoardMove(board_queen_e4, 'e4e7')
        result = move.process()

        assert move.square_selectors_between() == ['e5', 'e6']
        assert result


class TestBoardRules():
    """ Test specific board rules defined in legal_move(). """

    def test_pawncapture(self, board_fixt):
        """ Test the possibility for pawns to move horizontally. """
        move = BoardMove(board_fixt.board, 'e4f5')
        board_fixt.place_piece(pieces.Pawn(colors.WHITE), 'e4')
        board_fixt.place_piece(pieces.Rook(colors.BLACK), 'f5')

        valid = move.process()

        assert valid
        assert isinstance(
            valid.squares['f'][5].occupant, pieces.Pawn)

    def test_pawn_no_move_backwards(self, board_fixt):
        """Test if pawns can't move backwards."""
        move = BoardMove(board_fixt.board, 'c3c2')
        board_fixt.place_piece(pieces.Pawn(colors.WHITE), 'c3')

        assert not move.process()

    def test_pawn_no_forward_capture(self, board_fixt):
        """Test if it's not possible for pawns to capture forward."""
        board_fixt.place_piece(pieces.Pawn(colors.WHITE), 'c3')
        board_fixt.place_piece(pieces.Rook(colors.BLACK), 'c4')

        move = BoardMove(board_fixt.board, 'c3c4')

        assert not move.process()

    def test_defending_check(self, board_fixt):
        """Test if it's possible to defend check by placing a piece between."""
        move = BoardMove(board_fixt.board, 'c8d7')

        board_fixt.place_piece(pieces.Bishop(colors.WHITE), 'c8')
        board_fixt.place_piece(pieces.Bishop(colors.BLACK), 'b5')
        board_fixt.place_piece(pieces.King(colors.WHITE), 'e8')

        assert board_fixt.board.is_check(color=colors.WHITE)
        assert move.process(debug=True)

    def test_pawn_no_backward_capture(self, board_fixt):
        """Test if it's not possible for pawns to capture backwards."""
        board_fixt.place_piece(pieces.Rook(colors.WHITE), 'c3')
        board_fixt.place_piece(pieces.Pawn(colors.BLACK), 'c4')

        move = BoardMove(board_fixt.board, 'c4c3')

        assert not move.process()

    @pytest.mark.parametrize(
        "white_pos,black_pos,move,expected,vertical_steps", [
            # Black to move left
            ('c4', 'd4', 'd4c3', True, 2),
            ('c4', 'd4', 'd4c3', False, 1),
            ('c2', 'd4', 'd4c3', False, 2),
            # Black to move right
            ('e4', 'd4', 'd4e3', True, 2),
            ('e4', 'd4', 'd4e3', False, 1),
            ('e2', 'd4', 'd4e3', False, 2),
            # White to move left
            ('d5', 'c5', 'd5c6', True, 2),
            ('d5', 'c5', 'd5c6', False, 1),
            ('d5', 'c7', 'd5c6', False, 2),
            # White to move right
            ('d5', 'e5', 'd5e6', True, 2),
            ('d5', 'e5', 'd5e6', False, 1),
            ('d5', 'e7', 'd5e6', False, 2),
        ])
    def test_enpassant(self, board_fixt, white_pos, black_pos,
                       move, expected, vertical_steps):
        """ Test enpassant rules. """
        white_piece = pieces.Pawn(colors.WHITE)
        black_piece = pieces.Pawn(colors.BLACK)
        white_piece.last_move = SimpleNamespace(vertical=vertical_steps)
        black_piece.last_move = SimpleNamespace(vertical=vertical_steps)

        board_fixt.place_piece(white_piece, white_pos)
        board_fixt.place_piece(black_piece, black_pos)

        for pos in (white_pos, black_pos):
            if not move[:2] == pos:
                pass_pos = pos

        move = BoardMove(board_fixt.board, move)

        # Test if the boardrules are valid or not as we expect
        assert move.valid == expected

        if expected:
            # Test the amount of allowed moves for the moving piece
            assert len(move.origin_sq.occupant.allowed_moves(
                board=board_fixt.board)) == 2
            # Test whether the piece we're capturing is actually gone
            assert not move.process(
            ).squares[pass_pos[0]][int(pass_pos[1])].occupant
        else:
            # Test the amount of allowed moves for the moving piece
            assert len(move.origin_sq.occupant.allowed_moves(
                board=board_fixt.board)) == 1

    @pytest.mark.parametrize("move,expected", [
        # Can we move through other colored pieces?
        ('g5e7', False),
        # Can we move through our own pieces?
        ('c5e7', False),
    ])
    def test_blocked(self, board_fixt, move, expected):
        """ Test rules for blocked pieces work correctly. """
        board_fixt.place_piece(pieces.Pawn(colors.BLACK), 'd6')
        board_fixt.place_piece(pieces.Bishop(colors.WHITE), 'g5')
        board_fixt.place_piece(pieces.Pawn(colors.BLACK), 'f6')
        board_fixt.place_piece(pieces.Bishop(colors.BLACK), 'c5')
        move = BoardMove(board_fixt.board, move)

        result = move.process()

        assert result == expected

    @pytest.mark.parametrize("move,expected", [
        ('f5e7', False),
        ('e4d4', Board),
    ])
    def test_selfchecking(self, board_fixt, move, expected):
        """ Confirm it's not possible to place self in check. """
        board_fixt.place_piece(pieces.King(colors.WHITE), 'e4')
        board_fixt.place_piece(pieces.Knight(colors.WHITE), 'f5')
        board_fixt.place_piece(pieces.Queen(colors.BLACK), 'g6')
        boardmove = BoardMove(board_fixt.board, move)
        result = boardmove.process()

        if isinstance(expected, bool):
            assert result == expected
        else:
            assert isinstance(result, expected)

    @pytest.mark.parametrize("move,expected,side,color", [
        # Queenside castle for white with no checks etc.
        ('e1a1', True, 'queenside', colors.WHITE),
        # Same as above but differnt notation
        ('e1b1', True, 'queenside', colors.WHITE),
        # Black kingside no checks etc.
        ('e8h8', True, 'kingside', colors.BLACK),
        # White kingside, checked by bishop
        ('e1h1', False, 'kingside', colors.WHITE),
        # Black queenside, checked by bishop on ending square
        ('e8a8', False, 'queenside', colors.BLACK),
    ])
    def test_castling(self, board_fixt, move, expected, side, color):
        """ Test different castling scenario's """
        board_fixt.place_piece(pieces.King(colors.WHITE), 'e1')
        board_fixt.place_piece(pieces.Rook(colors.WHITE), 'a1')
        board_fixt.place_piece(pieces.Rook(colors.WHITE), 'h1')
        board_fixt.place_piece(pieces.King(colors.BLACK), 'e8')
        board_fixt.place_piece(pieces.Rook(colors.BLACK), 'a8')
        board_fixt.place_piece(pieces.Rook(colors.BLACK), 'h8')
        board_fixt.place_piece(pieces.Bishop(colors.BLACK), 'h3')
        board_fixt.place_piece(pieces.Bishop(colors.WHITE), 'f5')

        boardmove = BoardMove(board_fixt.board, move)

        result = boardmove.process()

        if expected:
            board = result.squares
            if side == 'kingside':
                r_char = 'f'
                k_char = 'g'

            else:
                r_char = 'd'
                k_char = 'c'

            if color == colors.WHITE:
                row = 1
            else:
                row = 8

            assert isinstance(board[k_char][row].occupant, pieces.King)
            assert isinstance(board[r_char][row].occupant, pieces.Rook)

        else:
            assert result == expected

    @pytest.mark.parametrize("move,expected", [
        # Queenside castle for white with a bishop in the way.
        ('e1a1', False),
    ])
    def test_castling_blocked(self, board_fixt, move, expected):
        """ Test if we can castle through others. """
        board_fixt.place_piece(pieces.King(colors.WHITE), 'e1')
        board_fixt.place_piece(pieces.Bishop(colors.WHITE), 'b1')
        board_fixt.place_piece(pieces.Rook(colors.WHITE), 'a1')

        boardmove = BoardMove(board_fixt.board, move)

        result = boardmove.process()

        assert result == expected
