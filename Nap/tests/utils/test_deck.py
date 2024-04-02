from pathlib import Path
import sys
import unittest

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Card,
    Suit,
    Deck,
)

class TestDeck(unittest.TestCase):
    """Deck class test.
    """
    def test_init_deck(self):
        """Test deck.
        """
        deck = Deck()
        deck.shuffle()
        assert len(deck) == 54

        print(deck.cards[0].image_url)
        print(deck.cards[0].suit)
        
        hand = deck.deal(10)
        print([str(card) for card in hand])
        
    def test_pull_out(self):
        """
        pull out method のテスト
        """
        deck = Deck()
        deck.cards = deck.cards[:5]
        assert str(deck) == str(['1 ♠', '1 ♥', '1 ♦', '1 ♣', '2 ♠'])

        target = Card(num = 1, suit = Suit.spade)
        deck.pull_out([target])
        # assert str(deck) == str(['1 ♥', '1 ♦', '1 ♣', '2 ♠'])

        # cards = deck.deal(num = 1)
        print(deck)
        # print(cards[0])

        deck.pull_out([target])
        print(deck)

if __name__ == '__main__':
    unittest.main()
