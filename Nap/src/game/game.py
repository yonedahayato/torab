from ..field import (
    Field,
)

from .track import Track

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

    def __init__(self, field: Field):
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
        self.field = field
        
    def shuffle(self):
        """Shuffle a deck.
        """
        self.field.deck.shuffle()
        
    def deal(self):
        """Deal cards.
        カードを各プレイヤーに配る
        あまったカードはウィドーに置く
        """
        for player in self.field.players:
            player.take_hand(self.field.deck.deal(self.hand_num))

        self.field.widow = self.field.deck.deal(self.widow_num)

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
