from pathlib import Path
import sys
from typing import Callable

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Deck,
)

from src.field import (
    Field
)

from src.player import (
    Player
)

def test_field(data_dir: str, players: Callable[[list[str]], list[Player]]):
    """
    フィールドクラスのテスト
    
    Args:
        data_dir (str): 結果を出力するためのディレクトリ
    """
    deck = Deck()
    two_players = players(player_names=["A", "B"])
    field = Field(deck, two_players)
    print(field)
    image_path = Path(data_dir) / "test_field.jpg"
    field.make_image(save_path=image_path)