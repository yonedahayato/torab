import io
from pathlib import Path
import pytest
import sys

from _pytest.monkeypatch import MonkeyPatch

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Suit,
    Card,
)

from src.game import (
    VSBase,
    SimpleNapVSTakeshi,
    EasyNapVSTakeshi,
)

ENDING = """##################################################
#
#\t\t\t山札: 42
#\t\t\t捨て札: 10
#\t\t\t場: 0
#\t\t\t切り札: {trump}
#
#\tPlayers
#\t\tたけし ({point_01}): []
#\t\tYou ({point_02}): []
#
#\tMessage
#\t\tこのゲームの勝者は、{winner} です
#
#
##################################################
"""

class TestVSBase:
    """
    VSBase クラスのテスト
    """
    def test_raise_set_player(self):
        """
        VSBase クラスをインスンス化して、_set_player method を実行して、NotImplementedErrorを確認する
        """
        with pytest.raises(NotImplementedError):
            VSBase()._set_player()

@pytest.fixture()
def hand_fixed_on_easy_nap_vs_takeshi() -> EasyNapVSTakeshi:
    """
    EasyNapVSTakeshi のゲームにて、プレイヤーの手札を固定したフィールを作成する
    """
    game = EasyNapVSTakeshi()
    takeshi_hand = [Card(num = n, suit = Suit.club) for n in range(1, 1 + game.hand_num)]
    player_hand = [Card(num = n, suit = Suit.spade) for n in range(1, 1 + game.hand_num)]

    for player in game.field.players:
        if str(player) == "たけし":
            player.take_hand(takeshi_hand)
        else:
            player.take_hand(player_hand)
            
    return game

class TestSimpleNapVSTakeshi:
    """
    SimpleGameVSTakeshi class のテスト
    """
    def test_play(self, monkeypatch: MonkeyPatch):
        """
        ゲームの実行のテスト

        Args:
            monkeypatch (MonkeyPatch): pytest tool
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("0\n0\n0\n"))
        game = SimpleNapVSTakeshi()
        game.play()
        
class TestEasyNapVSTakeshi:
    """
    EasyGameVSTakeshi class のテスト

    Args:
        monkeypatch (MonkeyPatch): pytest tool
    """
    def test_init(self):
        """
        クラスのインスタンスのテスト

        Args:
            monkeypatch (MonkeyPatch): pytest tool
        """
        game = EasyNapVSTakeshi()

    def test_play(self, 
                  monkeypatch: MonkeyPatch, 
                  capsys,
                  hand_fixed_on_easy_nap_vs_takeshi: EasyNapVSTakeshi):
        """
        ゲームの実行のテスト

        Args:
            monkeypatch (MonkeyPatch): pytest tool
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("0\n0\n0\n0\n0\n"))
        game = hand_fixed_on_easy_nap_vs_takeshi
        game.play()

        captured = capsys.readouterr()

        winner = game.decide_winner_in_game()
        expected = ENDING.format(trump = game.field.trump.mark,
                                 winner = str(winner),
                                 point_01 = game.field.players[0].point,
                                 point_02 = game.field.players[1].point)

        assert captured.out.split("\n\n")[-1] == expected