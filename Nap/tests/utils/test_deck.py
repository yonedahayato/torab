from pathlib import Path
import pytest
import sys

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Card,
    Suit,
    Deck,
)

class TestDeck:
    """
    Deck class のテスト
    """
    def test_init(self):
        """
        Deck class の init のテスト
        """
        deck = Deck()

    def test_len(self):
        """
        len のテスト
        """

        deck = Deck()
        assert len(deck) == 54
        
    def test_shuffle(self):
        """
        shuffle のテスト
        """
        deck = Deck()
        deck.shuffle()
        
    def test_deal(self):
        """
        deal のテスト
        """
        deck = Deck()        
        hand = deck.deal(10)
        assert len(hand) == 10
        
    def test_pull_out(self):
        """
        pull out method のテスト
        """
        deck = Deck()
        deck.cards = deck.cards[:5]
        assert str(deck) == str(['♠-A', '♥-A', '♦-A', '♣-A', '♠-2'])

        target = Card(num = 1, suit = Suit.spade)
        deck.pull_out([target])
        assert str(deck) == str(['♥-A', '♦-A', '♣-A', '♠-2'])

        with pytest.raises(ValueError):
            deck.pull_out([target])