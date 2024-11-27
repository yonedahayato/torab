import io
from pathlib import Path
import pytest
import sys
from _pytest.monkeypatch import MonkeyPatch

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    SimpleDeck,
)

from src.player import (
    Player,
)

from src.field import (
    Field,
)

from src.bid import (
    NapBid,
    NapDeclaration,
)

class PassBitPlayer(Player):
    """
    ビットにて必ずパスを宣言するプレイヤー
    """
    def declare(self, 
                declarable_list: list,
                is_random: bool = False,
            ) -> any:
        """Declare.
        宣言する
        
        Args:
            declarable_list (list): 宣言可能な一覧
            is_random (bool): ランダムに宣言するかどうか

        Returns:
            Declear: 宣言

        Note:
            ランダム or CPU ならば、ランダムに宣言を行う
        """

        return NapDeclaration("pass")

@pytest.fixture
def pass_bit_players() -> Player:
    """
    必ずパスをするプレイヤー達を準備する
    """
    alice = PassBitPlayer(name = "alice", cpu = True)
    bob = PassBitPlayer(name = "bob", cpu = True)

    return alice, bob

class TestNapDeclaration:
    """
    NapDeclaration class のテスト
    """
    def test_raise_nap_declaration(self):
        """
        名称の異常の確認のテスト
        """
        with pytest.raises(ValueError) as e:
            dec = NapDeclaration("xx")
        assert str(e.value) == "NapDeclaration において、異常なビッド: xx"
    def test_init_nap_declaration(self):
        """
        NapDeclaration の初期化のテスト
        """
        dec = NapDeclaration("two")
        assert dec.name == "two"
        assert dec.d_value == 1
    
    def test_is_pass(self):
        """
        パスをしたかどうかの判定のテスト
        """
        dec = NapDeclaration("pass")
        assert dec.is_pass()
        dec = NapDeclaration("two")
        assert not dec.is_pass()
    
    def test_is_declared(self):
        """
        宣言を一度でもしたかどうかの判定のテスト
        """
        dec = NapDeclaration("no_declare")
        assert not dec.is_declared()
        dec = NapDeclaration("two")
        assert dec.is_declared()
    
    def test_get_declarable_list(self):
        """
        自身のディクレアに対してコールできるディクレアの一覧を返すテスト
        """
        dec = NapDeclaration("two")
        declarable_list = dec.get_declarable_list()
        assert len(declarable_list) == 6
        assert declarable_list[0].name == "pass"
        assert declarable_list[1].name == "three"
        assert declarable_list[2].name == "misere"
        assert declarable_list[3].name == "four"
        assert declarable_list[4].name == "nap"
        assert declarable_list[5].name == "wellington"

class TestNapBid:
    """
    NapBid class のテスト
    """
    def test_nap_bid(self,
                     pass_bit_players,
                     monkeypatch: MonkeyPatch):
        """
        NapBid class の実行のテスト
        プレイヤーが two をコールし
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("1\n"))

        alice, bob = pass_bit_players
        deck = SimpleDeck()
        players = [
            alice,
            bob,
            Player("You", cpu=False)
        ]
        field = Field(deck, players)
        field.deck.shuffle()

        hand_num = 5
        for player in field.players:
            player.take_hand(field.deck.deal(hand_num))

        nap_bid = NapBid(field)
        for field_tmp in nap_bid:
            print(field_tmp)

        assert nap_bid.is_finish_flag
        assert nap_bid.declarer.name == "You"
        assert nap_bid.invalid == False

    def test_nap_bid_everyone_pass(self, 
                                   pass_bit_players,
                                   monkeypatch: MonkeyPatch):
        """
        全員がパスをしたときのテスト
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("0\n"))

        alice, bob = pass_bit_players
        deck = SimpleDeck()
        players = [
            alice,
            bob,
            Player("You", cpu=False)
        ]

        field = Field(deck, players)
        field.deck.shuffle()

        hand_num = 5
        for player in field.players:
            player.take_hand(field.deck.deal(hand_num))

        nap_bid = NapBid(field)
        for field_tmp in nap_bid:
            print(field_tmp)

        assert nap_bid.is_finish_flag
        assert nap_bid.invalid

        
