import pytest
from nerdchess.game import ChessGame
from nerdchess.player import Player
from nerdchess.board import Board
from nerdchess.config import colors
from nerdchess import pieces


@pytest.fixture(scope='class')
def chessgame():
    (player_1,
     player_2) = Player.create_two('blaat', 'henk', 'r')

    game = ChessGame(player_1, player_2)

    return game


class TestGame():
    """
    Tests the setup and basic functionality of a game.
    """

    def test_setup(self, chessgame):
        """ Test for expected contents of the game. """
        # Are the players who they're supposed to be?
        assert isinstance(chessgame.player_1, Player)
        assert isinstance(chessgame.player_2, Player)
        assert isinstance(chessgame.playerlist, list)
        assert chessgame.player_1.name == 'blaat'
        assert chessgame.player_2.name == 'henk'
        if chessgame.player_1.color == colors.WHITE:
            assert chessgame.player_2.color == colors.BLACK
        else:
            assert chessgame.player_1.color == colors.BLACK
            assert chessgame.player_2.color == colors.WHITE

        # Do we have a board?
        assert isinstance(chessgame.board, Board)

        # Do we have pieces and pawns?
        assert len(chessgame.pieces) == 16
        assert len(chessgame.pawns) == 16

    def test_move(self, chessgame):
        """ Do moves process correctly? """
        # White should start
        player = 'henk'
        for dude in chessgame.playerlist:
            if dude.color == colors.WHITE:
                player = dude
                assert dude.turn
            else:
                assert not dude.turn

        # Shouldn't be able to move the other players' pawn
        faulty_move = chessgame.move(player, 'e7e5')
        assert not faulty_move

        # Should be able to move my own pawn
        result = chessgame.move(player, 'e2e4')
        assert result

        # We should be keeping history
        assert len(chessgame.board_history) == 1

        # After a succesful move the turn is passed
        for dude in chessgame.playerlist:
            if dude.color == colors.BLACK:
                assert dude.turn
            else:
                assert not dude.turn

    def test_promote(self, chessgame, board_fixt):
        """Test pawn promotion."""
        for player in chessgame.playerlist:
            if player.color == colors.WHITE:
                player.turn = True
                player_white = player

        pawn = pieces.Pawn(colors.WHITE)
        board_fixt.place_piece(pawn, 'e7')
        chessgame.board = board_fixt.board

        result = chessgame.move(player_white, 'e7e8')
        assert result.promotion

        pawn = chessgame.board.squares['e'][8].occupant
        result = chessgame.promote(pawn, pieces.Queen)
        assert isinstance(chessgame.board.squares['e'][8].occupant,
                          pieces.Queen)


class TestMatch():
    """
    Test a complete match between two players!
    """

    @pytest.mark.parametrize("move,game_over", [
        ('e2e4', False),
        ('e7e5', False),
        ('f1c4', False),
        ('f8a3', False),
        ('g1f3', False),
        ('b8a6', False),
        ('f3e5', False),
        ('c7c6', False),
        ('d1f3', False),
        ('d7d5', False),
        ('f3f7', True),
    ])
    def test_match(self, chessgame, move, game_over):
        current_player = 'henk'
        for player in chessgame.playerlist:
            if player.turn:
                current_player = player

        result = chessgame.move(current_player, move)

        assert(result)
        assert(chessgame.over == game_over)
