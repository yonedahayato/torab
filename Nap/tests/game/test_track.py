import sys
from pathlib import Path
from typing import Callable

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

def test_track(players: Callable[[list[str]], list[Player]]):
    """Test track.
    トラックのテスト
    
    Args:
        players (list[Player]): 参加するプレイヤー
    """
    deck = Deck()
    players = players()
    field = Field(deck, players)

    game = Game(field = field)
    game.shuffle()
    game.deal()
    game.field.trump = Suit.spade

    field = game.field
    track = Track(field = field)
    winner = track.play(display=True)
    
    print(f"Winner is {winner}")

if __name__ == '__main__':
    test_track()