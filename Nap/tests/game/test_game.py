from pathlib import Path
import pytest
import sys

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Suit,
    Card,
)

from src.game import (
    Game,
    SimpleNapGame,
    EasyNapGame,
)

from src.player import (
    Player,
)

class TestGame:
    """
    Game クラスのテスト
    """
    def test_init(self):
        """
        Game クラスのインスタンスのテスト

        Note:
            _set_trump メソッドが実装されていないため、NotImplementedError が発生する
        """
        with pytest.raises(NotImplementedError):
            game = Game()

class TestSimpleNapGame:
    """
    SimpleNapGame class のテスト
    """
    def test_init(self):
        """
        SimpleNapGame クラスのインスタンスのテスト

        Note:
            以下の method の動作を確認できる
                - set_deck
                - _set_player
                - shuffle
                - deal
                - _set_trump
                - set_track
        """
        game = SimpleNapGame()
        assert game.hand_num == 3
        assert game.field.trump == Suit.spade

    def test_get_start_player_id(self):
        """
        get_start_player_id method のテスト
        """
        game = SimpleNapGame()
        assert game.get_start_player_id() == 0

    def test_add_point(self):
        """
        add_point method のテスト
        """
        game = SimpleNapGame()
        player_boss = game.field.players[0]
        game.add_point(player_boss)
        assert player_boss.point == 1

    def test_play(self, capfd):
        """
        play method のテスト

        Args:
            capfd (_pytest.capture.CaptureFixture): 標準出力を確認するためのツール
        """
        game = SimpleNapGame()
        captured = capfd.readouterr()
        output_texts: str = captured.out

        targets = [
            "52 枚のカードを使用します",
            str(game.field) + "\n",
        ]
        for cnt, output_text in enumerate(output_texts.split("\n\n")):
            if cnt == 1:
                print(output_text)
            assert targets[cnt] == output_text

    def test_calculate_strongness(self):
        """
        calculate_strongness メソッドのテスト
        """
        game = SimpleNapGame()
        assert game.calculate_strongness(Card(num=1, suit=Suit.spade)) == (14, 6)
        assert game.calculate_strongness(Card(num=10, suit=Suit.heart)) == (10, 3)
        assert game.calculate_strongness(Card(num=2, suit=Suit.club)) == (2, 1)

    def test_decide_winner_in_track(self):
        """
        decide_winner_in_track メソッドのテスト
        """
        game = SimpleNapGame()
        game.field.cards = {
            "Boss": Card(num=1, suit=Suit.spade),
            "You": Card(num=10, suit=Suit.heart),
        }
        winner = game.decide_winner_in_track()
        assert winner.name == "Boss"

    def test_decide_winner_in_game(self):
        """
        decide_winner_in_game メソッドのテスト
        """
        game = SimpleNapGame()
        game.field.players = [
            Player("Boss"),
            Player("You"),
        ]
        game.field.players[0].point = 1
        game.field.players[1].point = 2

        winner = game.decide_winner_in_game()
        assert winner.name == "You"

class TestEasyNapGame:
    """
    EasyNapGame class のテスト
    """
    def test_init(self):
        """
        EasyNapGame クラスのインスタンスのテスト
        """
        game = EasyNapGame()
        assert game.hand_num == 5
        assert game.field.is_use_lead is True
        assert game.field.trump in [Suit.spade, Suit.heart, Suit.diamond, Suit.club]

    def test_get_start_player_id(self):
        """
        get_start_player_id メソッドのテスト
        """
        game = EasyNapGame()
        assert game.get_start_player_id() in [0, 1]
        game.track_cnt = 1
        game.winner_id_in_track = 0
        assert game.get_start_player_id() == 0

    def test_calculate_strongness(self):
        """
        calculate_strongness メソッドのテスト
        """
        game = EasyNapGame()
        game.field.trump = Suit.spade
        game.field.cards = {"Boss": Card(num=10, suit=Suit.heart)}
        assert game.calculate_strongness(Card(num=1, suit=Suit.spade)) == (14, 6)
        assert game.calculate_strongness(Card(num=10, suit=Suit.heart)) == (10, 5)
        assert game.calculate_strongness(Card(num=2, suit=Suit.club)) == (2, 1)