import random
from typing import Any

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
                    a. この宣言にて、ナポレオンが決まる
                    b. ナポレオンが宣言したスートが切り札となる
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
        for _ in range(10):
            track = Track(self.deck, self.players, self.field)
            track.play()
            self.field.clear()

class Track:
    """1 回のゲームを管理するクラス
    
    Note:
        このクラスでは、以下のことを行う
        1. トラックの処理の実行
        2. そのトラックにおける勝者の決定
    """
    def __init__(self, players: list[Player], field: Field):
        """Constructor.
        """
        self.players = players
        self.field = field
        
    def play(self, is_random: bool = False, display: bool = False, is_first: bool = False):
        """Play a trak.
        
        Args:
            is_random (bool): ランダムにカードを出すかどうか
            display (bool): 出したカードを表示するかどうか
            is_first (bool): 最初のプレイかどうか

        Note:
            トラックの流れは以下の通り
                1. 各プレイヤーがカードを出す
                2. 出されたカードの強さを比較する

            最初のトラックは、特殊なカードの効果が発動しない
        """
        for player in self.players:
            card = player.play_card(self.field, is_random = is_random)
            if display:
                print(f"{player} が {card} を出した")

            self.field.put_card(player.name, card)

        print(f"\n場に出たカードは {[name + ' : ' + str(c) for name, c in self.field.cards.items()]} です")
        self.field.show()
        
        winner = self.winner()
        return winner
        
    def winner(self) -> Player:
        """Decide a winner.
        勝者を決める
        
        Returns:
            Player: 勝者
            
        Note:
            各プレイヤーがフィールドに出したカードの強さを比較して、勝者を決める
        """
        winner_card = max(list(self.field.cards.values()), 
                          key = lambda x: (self.field.suit_strength(x.suit), x.num))
        
        def get_key(dictionary, value):
            """value から key を取得する
            """
            for k, v in dictionary.items():
                if str(v) == str(value):
                    return k
            return None

        winner = get_key(self.field.cards, winner_card)
        return winner
