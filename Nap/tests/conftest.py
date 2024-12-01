from pathlib import Path
import pytest
import sys
from typing import Callable

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.player import Player
from src.utils import (
    Deck,
    Card,
    Suit,
)
from src.field import Field
from src.bid import (
    NapDeclaration,
)

@pytest.fixture
def data_dir() -> str:
    """
    テストの結果出力などに使う共通のディレクトリを参照する
    
    Returns:
        str: データディレクトリのパス
    """
    _data_dir = FILE_DIR / "data"
    _data_dir.mkdir(exist_ok=True)
    return str(_data_dir)

# player 系

class PassBitPlayer(Player):
    """
    ビットにて必ずパスを宣言するプレイヤー
    """
    def declare(self, 
                declarable_list: list,
                is_random: bool = False,
            ) -> any:
        """Declare.
        宣言する
        
        Args:
            declarable_list (list): 宣言可能な一覧
            is_random (bool): ランダムに宣言するかどうか

        Returns:
            Declear: 宣言

        Note:
            ランダム or CPU ならば、ランダムに宣言を行う
        """

        return NapDeclaration("pass")

@pytest.fixture
def players() -> Callable[[list[str]], list[Player]]:
    """
    ゲームに参加するプレイヤー
    
    Returns:
        callable: ゲームに参加するプレイヤーを作成する関数
    
    """
    def _players(player_names: list[str] = ["A", "B", "C", "D"]) -> list[Player]:
        """
        ゲームに参加するプレイヤーを作成する

        Args:
            player_names (list[str]): プレイヤー達の名前
            
        Returns
            list[Player]: プレイヤー達
        """

        return [PassBitPlayer(name, cpu=True) for name in player_names if name != "You"] + [Player("You", cpu=False)]

    return _players

@pytest.fixture
def pass_bit_players() -> Callable[[list[str]], list[Player]]:
    """
    必ずパスをするプレイヤー達を準備する

        Returns:
        callable: ゲームに参加するプレイヤーを作成する関数
    """
    def _players(player_names: list[str] = ["A", "B"]) -> list[Player]:
        """
        ゲームに参加するプレイヤーを作成する

        Args:
            player_names (list[str]): プレイヤー達の名前
            
        Returns
            list[Player]: プレイヤー達
        """
        return [PassBitPlayer(name, cpu=True) for name in player_names if name != "You"] + [Player("You", cpu=False)]

    return _players

# field 系

@pytest.fixture
def field_with_cpu_players(
    players: Callable[[list[str]], list[Player]],
    ) -> Callable[dict[str, list[Card]], Field]:
    """
    CPU のプレイヤーが居る状態のフィールド

    Args:
        players (Callable[[list[str]], list[Player]]): プレイヤーを返す関数

    Returns:
        Field を返す関数
    """
    hands_set1 = [Card(num, Suit.club) for num in range(1, 4)]
    hands_set2 = [Card(num, Suit.heart) for num in range(1, 4)]
    hands_set3 = [Card(num, Suit.spade) for num in range(1, 4)]
    def _field(
            players_with_hand: dict = {"A": hands_set1, "B": hands_set2, "You": hands_set3},
            ) -> Field:
        """
        CPU のプレイヤーが居る状態のフィールドを準備する
        """
        deck = Deck()
        _players = players(player_names=list(players_with_hand.keys()))
        field = Field(deck, _players)
        for player in field.players:
            print(player)
            hands = players_with_hand[str(player)]
            hands_tmp = field.deck.pull_out(hands)
            player.take_hand(hands_tmp)

        return field

    return _field

@pytest.fixture
def field_two_cpu_payers(players: Callable[[list[str]], list[Player]]):
    """
    CPU のプレイヤーが 2 人居る状態のフィールド
    
    Args:
        players (Callable[[list[str]], list[Player]]): プレイヤーを作成する関数
        
    Returns:
        Field: フィールド
    """
    deck = Deck()
    two_players = players(player_names=["A", "B"])
    
    return Field(deck, two_players)

@pytest.fixture
def field_two_cpu_payers_dealed(field_two_cpu_payers: Field):
    """
    CPU が二人居り、カードが配り終えた状態のフィールド
    
    Returns:
        Field: フィールド

    Note:
        配るカードはランダム
    """
    field_two_cpu_payers.deck.shuffle()
    for player in field_two_cpu_payers.players:
        hand = field_two_cpu_payers.deck.deal(num = 3)
        player.take_hand(hand)
        
    return field_two_cpu_payers