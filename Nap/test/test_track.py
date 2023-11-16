import sys
from pathlib import Path

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from utils import (
    Deck,
    Field,
)

from game import (
    Track,
    Game,
)

from player import (
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
    
    plyers = game.players
    field = game.field
    track = Track(players = plyers, field = field)
    track.play(is_random=True, display=True)

if __name__ == '__main__':
    test_track()