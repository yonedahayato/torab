from pathlib import Path
import pytest
import sys

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


class TestNapBid:
    """
    NapBid class のテスト
    """
    def test_nap_bid(self):
        """
        NapBid class の実行のテスト
        """
        deck = SimpleDeck()
        players = [
            Player("Alice", cpu=True), 
            Player("Boss", cpu=True), 
            Player("You", cpu=False)
        ]
        field = Field(deck, players)
        field.deck.shuffle()

        hand_num = 5
        for player in field.players:
            player.take_hand(field.deck.deal(hand_num))

        nap_bid = NapBid(field)