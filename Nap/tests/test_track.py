import sys
from pathlib import Path

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Deck,
    Field,
    Suit,
)

from src.game import (
    Track,
    Game,
)

from src.player import (
    Player,
)

def test_track():
    """Test track.
    トラックのテスト
    """
    player_names = ["A", "B", "C", "D"]
    players = [Player(name, cpu=True) for name in player_names] + [Player("You", cpu=False)]
    deck = Deck()
    field = Field()

    game = Game(players = players, deck = deck, field = field)
    game.shuffle()
    game.deal()
    game.field.set_trump(Suit.spade)
    
    plyers = game.players
    field = game.field
    track = Track(players = plyers, field = field)
    winner = track.play(is_random=True, display=True)
    
    print(f"Winner is {winner}")

if __name__ == '__main__':
    test_track()