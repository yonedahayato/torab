from pathlib import Path
import pytest
import sys

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Card,
    Suit,
)

class TestCard:
    """
    カードクラスのテスト
    """
    def test_init(self):
        """
        カードクラスのinitのテスト
        """
        spade_1 = Card(1, Suit.spade)
        assert str(spade_1) == "♠-A"

    def test_image_url(self):
        """
        カードの image_url 変数の確認
        """
        club_1 = Card(1, Suit.club)
        
        assert str(club_1) == "♣-A"
        assert club_1.image_url == "https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust14.png"

    def test_make_jocker(self):
        """
        ジョーカーカードの作成のテスト
        """
        strong_joker = Card(joker = 1)
        weak_joker = Card(joker = 2)

        assert str(strong_joker) == "Joker (strong)"
        assert str(weak_joker) == "Joker (weak)"

    def test_jocker_raises(self):
        """
        ジョーカーカードの例外のテスト
        """
        with pytest.raises(ValueError):
            error_joker = Card(joker = 3)
            
    def test_invalid_num_raises(self):
        """
        異常な数字のカードの作成を作成した時の例外のテスト
        """
        with pytest.raises(ValueError):
            error_card = weak_joker = Card(num = 14)

    def test_get_num_str(self):
        """
        get_num_str のテスト
        """
        spade_1 = Card(1, Suit.spade)
        assert spade_1.get_num_str() == "A"

def test_card_equality():
    card1 = Card(num = 1, suit = Suit.spade)
    card2 = Card(num = 1, suit = Suit.spade)
    card3 = Card(num = 2, suit = Suit.heart)
    assert card1 == card2
    assert card1 != card3

def test_card_comparison():
    card1 = Card(num=1, suit=Suit.spade)
    card2 = Card(num=2, suit=Suit.spade)
    card3 = Card(num=1, suit=Suit.heart)
    assert card1 < card2
    assert card3 < card2

def test_card_to_string():
    card1 = Card(num = 1, suit = Suit.spade)
    card2 = Card(num = 13, suit = Suit.heart)
    assert str(card1) == "♠-A"
    assert str(card2) == "♥-K"

def test_card_is_joker():
    card1 = Card(joker = 1)
    card2 = Card(num = 1, suit = Suit.spade)
    assert card1.is_joker()
    assert not card2.is_joker()

def test_card_path():
    card = Card(num=1, suit=Suit.heart)
    assert card.image_path.exists()