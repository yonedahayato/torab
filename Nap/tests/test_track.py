import sys
from pathlib import Path

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Deck,
    Suit,
)

from src.field import (
    Field,
)

from src.game import (
    Track,
    Game,
)

from src.player import (
    Player,
)

def test_track(players: list[Player]):
    """Test track.
    トラックのテスト
    
    Args:
        players (list[Player]): 参加するプレイヤー
    """
    deck = Deck()
    field = Field(deck, players)

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