from pathlib import Path
import sys
from typing import Callable
import pytest

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

FIELD_STR_CASE_01 = """
##################################################
#
#\t\t\t山札: 54
#\t\t\t場: 0
#\t\t\t捨て札: 0
#
#\tPlayers
#\t\tA: []
#\t\tB: []
#\t\tYou: []
#
##################################################"""

@pytest.fixture
def field_case_01(players: Callable[[list[str]], list[Player]]):
    deck = Deck()
    two_players = players(player_names=["A", "B"])
    
    return Field(deck, two_players)


class TestField:
    """
    フィールドクラスのテスト
    """
    def test_string_output(self, field_case_01: Field) -> None:
        """
        文字列を表示するメソッドのテスト
        
        Args:
            field_case_01 (Field): フィールのクラス
            
        Note:
            確認する状態
                1. カードとプレイヤーが集まり、フィールドができている状態
        """

        print(str(field_case_01))
        assert str(field_case_01) == FIELD_STR_CASE_01
        
    def test_image_outout(self, data_dir: str, players: Callable[[list[str]], list[Player]]) -> None:
        """
        画像を保存するメソッドのテスト
        
        Args:
            data_dir (str): 結果を出力するためのディレクトリ
            field_case_01 (Field): フィールのクラス
        """
        deck = Deck()
        two_players = players(player_names=["A", "B"])
        field = Field(deck, two_players)

        image_path = Path(data_dir) / "test_field.jpg"
        field.make_image(save_path=image_path)