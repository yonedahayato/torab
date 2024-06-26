from pathlib import Path
import pytest
import sys
from typing import Callable

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.player import Player
from src.utils import Deck
from src.field import Field

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

        return [Player(name, cpu=True) for name in player_names] + [Player("You", cpu=False)]

    return _players

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