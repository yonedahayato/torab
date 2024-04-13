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
