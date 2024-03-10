from pathlib import Path
import sys
import unittest

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Card,
    Suit,
)

class TestCard(unittest.TestCase):
    """Card class test.
    """
    def test_card(self):
        spade_1 = Card(1, Suit.spade)
        print(spade_1)
    
    def test_set_url(self):
        club_1 = Card(1, Suit.club)
        print(club_1)
        print(club_1.image_url)
        
    def test_draw(self):
        pass

if __name__ == '__main__':
    unittest.main()