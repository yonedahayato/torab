from pathlib import Path
import sys
import unittest

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from utils import (
    Card,
    Suit,
    Deck,
)

class TestDeck(unittest.TestCase):
    """Deck class test.
    """
    def test_deck(self):
        """Test deck.
        """
        deck = Deck()
        deck.shuffle()
        print(len(deck))
        print(deck.cards[0].url)
        print(deck.cards[0].suit)
        
        hand = deck.deal(10)
        print([str(card) for card in hand])
        
if __name__ == '__main__':
    unittest.main()
