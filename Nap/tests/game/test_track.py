import sys
from pathlib import Path
import pytest
from typing import Callable

FILEDIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILEDIR.parent.parent.absolute()
print(PROJECT_DIR)
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Deck,
    Suit,
)

from src.field import (
    Field,
)

from src.game import (
    SimpleTrack,
    NapTrack,
    Game,
    NapGame,
)

from src.player import (
    Player,
)

@pytest.fixture
def field_two_cpu_payers_dealed(field_two_cpu_payers: Field):
    """
    CPU が二人居り、カードが配り終えた状態のフィールド
    
    Returns:
        Field: フィールド
    """
    field_two_cpu_payers.deck.shuffle()
    for player in field_two_cpu_payers.players:
        hand = field_two_cpu_payers.deck.deal(num = 3)
        player.take_hand(hand)
        
    return field_two_cpu_payers

class TestSimpleTrack:
    """
    SimpleTrack のテスト
    """
    def test_play_track_using_for(self, field_two_cpu_payers_dealed: Field):
        """
        トラックの実行のテスト (__next__ method)
        """
        print(field_two_cpu_payers_dealed)
        simple_track = SimpleTrack(field = field_two_cpu_payers_dealed, 
                                   start_player_id = 0)

        for field in simple_track:
            print(field)

    def test_play_track_using_next(self, field_two_cpu_payers_dealed: Field):
        """
        トラックの実行のテスト (__next__ method)
        """
        print(field_two_cpu_payers_dealed)
        simple_track = SimpleTrack(field = field_two_cpu_payers_dealed, 
                                   start_player_id = 0)

        for _ in field_two_cpu_payers_dealed.players:
            field = next(simple_track)
            print(field)

class TestNapTrack:
    """
    NapTrack のテスト
    """
    def test_track(self, players: Callable[[list[str]], list[Player]]):
        """Test track.
        トラックの処理のテスト
        
        Args:
            players (list[Player]): 参加するプレイヤー
        """
        deck = Deck()
        players = players()
        field = Field(deck, players)

        game = NapGame(field = field)
        game.shuffle()
        game.deal()
        game.field.trump = Suit.spade

        field = game.field
        track = NapTrack(field = field, start_player_id = 0)
        winner = track.play(display=True)
        
        print(f"Winner is {winner}")