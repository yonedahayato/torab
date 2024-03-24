from pathlib import Path
import sys
import unittest

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Suit,
)

class TestSuit(unittest.TestCase):
    def test_suit(self):
        """Test suit.
        スートのテスト
        
        Note:
            スートの強さの順番を確認する
        """
        spade = Suit.spade
        heart = Suit.heart
        diamond = Suit.diamond
        club = Suit.club

        # spade
        assert spade == spade
        assert spade > heart
        assert spade > diamond
        assert spade > club
        
        # heart
        assert heart < spade
        assert heart == heart
        assert heart > diamond
        assert heart > club
        
        # diamond
        assert diamond < spade
        assert diamond < heart
        assert diamond == diamond
        assert diamond > club
        
        # club
        assert club < spade
        assert club < heart
        assert club < diamond
        assert club == club
        
    def test_suit_mark(self):
        """Test suit mark.
        スートのマークのテスト
        """
        spade = Suit.spade
        heart = Suit.heart
        diamond = Suit.diamond
        club = Suit.club
        
        assert spade.mark == "♠"
        assert heart.mark == "♥"
        assert diamond.mark == "♦"
        assert club.mark == "♣"

if __name__ == '__main__':
    unittest.main()