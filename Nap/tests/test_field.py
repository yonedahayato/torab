import io
from pathlib import Path
import pytest
import sys
from typing import Callable

from _pytest.monkeypatch import MonkeyPatch

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
    Player,
    Takeshi,
)

FIELD_STR_CASE_01 = """
##################################################
#
#\t\t\t山札: 54
#\t\t\t捨て札: 0
#\t\t\t場: 0
#
#\tPlayers
#\t\tA (0): []
#\t\tB (0): []
#\t\tYou (0): []
#
##################################################"""

FIELD_STR_CASE_02 = """
##################################################
#
#\t\t\t山札: 54
#\t\t\t捨て札: 0
#\t\t\t場: 0
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tA (0): []
#\t\tB (0): []
#\t\tYou (0): []
#
##################################################"""

FIELD_STR_CASE_03 = """
##################################################
#
#\t\t\t山札: 45
#\t\t\t捨て札: 0
#\t\t\t場: 0
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tA (0): ['?', '?', '?']
#\t\tB (0): ['?', '?', '?']
#\t\tYou (0): ['♠-4', '♠-5', '♠-6']
#
##################################################"""

FIELD_STR_CASE_04 = """
##################################################
#
#\t\t\t山札: 48
#\t\t\t捨て札: 0
#\t\t\t場: 0
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tたけし (0): ['♥-?', '?', '?']
#\t\tYou (0): ['♠-4', '♠-5', '♠-6']
#
##################################################"""

FIELD_STR_CASE_05 = """
##################################################
#
#\t\t\t山札: 48
#\t\t\t捨て札: 0
#\t\t\t場:
#\t\t\t\tたけし: {card}
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tたけし (0): ['♥-?', '?']
#\t\tYou (0): ['♠-4', '♠-5', '♠-6']
#
#\tMessage
#\t\t{player_name} が {card} を出した
#
#
##################################################"""

FIELD_STR_CASE_06 = """
##################################################
#
#\t\t\t山札: 48
#\t\t\t捨て札: 0
#\t\t\t場:
#\t\t\t\tたけし: {card_01}
#\t\t\t\tYou: {card}
#\t\t\t切り札: ♠
#
#\tPlayers
#\t\tたけし (0): ['♥-?', '?']
#\t\tYou (0): {hand}
#
#\tMessage
#\t\t{player_name} が {card} を出した
#
#
##################################################"""

@pytest.fixture
def field_with_takeshi():
    """
    CPU たけしが居る状態のフィールド

    Returns:
        Field: フィールド
        
    Note:
        hand_num (int): 配る枚数
    """
    deck = Deck()
    field = Field(deck, [Takeshi(), Player("You", cpu=False)])
    field.deck.shuffle()
    field.trump = Suit.spade

    hand_num = 3
    takeshi_hand = [Card(num = n, suit = Suit.heart) for n in range(1, 1 + hand_num)]
    my_hand = [Card(num = n, suit = Suit.spade) for n in range(4, 4 + hand_num)]

    for player in field.players:
        if player.name == "たけし":
            # deck からカードを引き抜く
            takeshi_hand = field.deck.pull_out(takeshi_hand)
            player.take_hand(takeshi_hand)
            
        else:
            my_hand = field.deck.pull_out(my_hand)
            player.take_hand(my_hand)
            
    return field

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

        assert str(field_two_cpu_payers) == FIELD_STR_CASE_03

    def test_str_with_takeshi(self, field_with_takeshi: Field) -> None:
        """
        文字列を表示するメソッドのテスト
        
        Args:
            field_with_takeshi (Field): フィールのクラス

        Note:
            確認する状態
                各プレイヤーにカードが分配できている状態
        """
        assert str(field_with_takeshi) == FIELD_STR_CASE_04

    def test_put_card(self, 
                      field_with_takeshi: Field,
                      monkeypatch: MonkeyPatch) -> None:
        """
        プレイヤーがカードを置く処理のテスト
        
        Args:
            field_with_takeshi (Field): たけしが待機しているフィールド
            monkeypatch (MonkeyPatch): pytest tool
                player のカードの提出時に、標準入力を利用
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("0\n"))

        for cnt, player in enumerate(field_with_takeshi.players):
            card = player.play_card()
            field_with_takeshi.put_card(player.name, card)
            field_with_takeshi.message = f"{player.name} が {card} を出した"
            
            if cnt == 0:
                card_tmp = card
                expected = FIELD_STR_CASE_05.format(card = str(card), 
                                                    player_name = str(player.name))
                assert str(field_with_takeshi) == expected
            elif cnt == 1:
                expected = FIELD_STR_CASE_06.format(card = str(card),
                                                    card_01 = str(card_tmp),
                                                    hand = [str(c) for c in player.cards],
                                                    player_name = str(player.name))
                assert str(field_with_takeshi) == expected

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