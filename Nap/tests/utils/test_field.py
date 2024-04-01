from pathlib import Path
import sys
from typing import Callable
import pytest

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Card,
    Deck,
    Suit,
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

FIELD_STR_CASE_02 = """
##################################################
#
#\t\t\t山札: 54
#\t\t\t場: 0
#\t\t\t捨て札: 0
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tA: []
#\t\tB: []
#\t\tYou: []
#
##################################################"""

FIELD_STR_CASE_03 = """
##################################################
#
#\t\t\t山札: 45
#\t\t\t場: 0
#\t\t\t捨て札: 0
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tA: ['?', '?', '?']
#\t\tB: ['?', '?', '?']
#\t\tYou: ['4 ♠', '5 ♠', '6 ♠']
#
##################################################"""

@pytest.fixture
def field_two_cpu_payers(players: Callable[[list[str]], list[Player]]):
    """
    CPU のプレイヤーが 2 人居る状態のフィールドクラス
    """
    deck = Deck()
    two_players = players(player_names=["A", "B"])
    
    return Field(deck, two_players)


class TestField:
    """
    フィールドクラスのテスト
    """
    def test_str_first_status(self, field_two_cpu_payers: Field) -> None:
        """
        文字列を表示するメソッドのテスト
        
        Args:
            field_two_cpu_payers (Field): フィールのクラス
            
        Note:
            確認する状態
                カードとプレイヤーが集まり、フィールドができている状態
        """

        print(str(field_two_cpu_payers))
        assert str(field_two_cpu_payers) == FIELD_STR_CASE_01
        
    def test_set_trump(selfself, field_two_cpu_payers: Field) -> None:
        """
        切り札を設置するメソッドのテスト
        
        Args:
            field_two_cpu_payers (Field): フィールのクラス
            
        Note:
            確認する状態
                切り札が決定しているフィールドの状態

        """
        field_two_cpu_payers.deck.shuffle()
        field_two_cpu_payers.trump = Suit.spade
        print(field_two_cpu_payers)
        assert str(field_two_cpu_payers) == FIELD_STR_CASE_02
        
    def test_str_deal_status(self, field_two_cpu_payers: Field, hand_num: int = 3) -> None:
        """
        文字列を表示するメソッドのテスト
        
        Args:
            field_two_cpu_payers (Field): フィールのクラス
            hand_num (int): 配る枚数

        Note:
            確認する状態
                各プレイヤーにカードが分配できている状態
        """
        field_two_cpu_payers.deck.shuffle()
        field_two_cpu_payers.trump = Suit.spade

        cpu_hands = {
            0: [Card(num = n, suit = Suit.heart) for n in range(1, 1 + hand_num)],
            1: [Card(num = n, suit = Suit.heart) for n in range(4, 4 + hand_num)],
        }
        my_hand = [Card(num = n, suit = Suit.spade) for n in range(4, 4 + hand_num)]

        cpu_cnt = 0
        for player in field_two_cpu_payers.players:
            if player.cpu:
                # deck からカードを引き抜く
                cpu_hand = field_two_cpu_payers.deck.pull_out(cpu_hands[cpu_cnt])
                player.take_hand(cpu_hand)
                cpu_cnt += 1
            else:
                my_hand = field_two_cpu_payers.deck.pull_out(my_hand)
                player.take_hand(my_hand)

        print(field_two_cpu_payers)
        assert str(field_two_cpu_payers) == FIELD_STR_CASE_03

    def test_image_outout(self, data_dir: str, players: Callable[[list[str]], list[Player]]) -> None:
        """
        画像を保存するメソッドのテスト
        
        Args:
            data_dir (str): 結果を出力するためのディレクトリ
            field_two_cpu_payers (Field): フィールのクラス
        """
        deck = Deck()
        two_players = players(player_names=["A", "B"])
        field = Field(deck, two_players)

        image_path = Path(data_dir) / "test_field.jpg"
        field.make_image(save_path=image_path)