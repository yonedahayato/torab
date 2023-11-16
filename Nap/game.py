import random

from player import Player
from utils import Suit, Card

from utils import (
    Deck,
    Field,
)

class Game:
    """A game of Nap.
    
    ゲームの進行を管理するクラス
    複数の Track を行う
    
    Attributes:
        hand_num (int): Number of cards to deal to each player.
        widow_num (int): Number of cards to deal to widow.
    """
    hand_num = 10
    widow_num = 4

    def __init__(self, players: list[Player], field: Field, deck: Deck):
        """Constructor.
        Note:
            ゲームの流れ
                1. デッキをシャッフルする
                2. デッキからカードを配る
                3. プレイヤーが強さを宣言する
                4. Track を 10回行う
                    a. プレイヤーがカードを出す
                    b. 出されたカードの強さを比較する
                    c. 強いカードを出したプレイヤーが勝ち
                5. プレイヤーの勝敗を決める
        """
        self.deck = deck
        self.players = players
        self.field = field
        
    def shuffle(self):
        """Shuffle a deck.
        """
        self.deck.shuffle()
        
    def deal(self):
        """Deal cards.
        カードを各プレイヤーに配る
        あまったカードはウィドーに置く
        """
        for player in self.players:
            player.take_hand(self.deck.deal(self.hand_num))

        self.field.set_widow(self.deck.deal(self.widow_num))

    def declare(self):
        """Declare a strength.
        自身のカードの強さを宣言する
        
        Note:
            1. 最初(親)のプレイヤーから宣言する
            2. 次のプレイヤーは前の宣言より強い宣言をする、またはパスする
            3. パスをしたら、そのプレイヤーは宣言できなくなる
            4. 全員パスしたら、ウィドーのカードを1枚公開し、そのカードのスートのJを持つプレイヤーがナポレオン
        """
        while True:
            strong_declear = None
            for player in self.players:
                declear = player.declare(strong_declear)

                if declear <= strong_declear:
                    pass
                else:
                    pass
                strong_declear = declear

    def play(self):
        """Play a game.
        """
        track = Track(self.deck, self.players, self.field)
        for _ in range(10):
            track.play()

class Track:
    """1 回のゲームを管理するクラス
    """
    def __init__(self, deck: Deck, players: list[Player], field: Field):
        """Constructor.
        """
        self.deck = deck
        self.players = players
        self.field = field
        
    def play(self, is_random: bool = False, display: bool = False):
        """Play a trak.
        
        Args:
            is_random (bool): ランダムにカードを出すかどうか
            display (bool): 出したカードを表示するかどうか

        Note:
            1. 各プレイヤーがカードを出す
            2. 出されたカードの強さを比較する
        """
        for player in self.players:
            card = player.play_card(self.field, is_random = is_random)
            if display:
                print(f"{player} が {card} を出した")
            self.field.put_card(card)
