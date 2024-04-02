from .player import Player
from ..utils import Suit

class Charactor(Player):
    """
    キャラクターのクラス
    """
    def talk(self):
        """
        キャラクターのセリフを出力する
        """
        raise NotImplementedError

class Takeshi(Charactor):
    """
    トランプ学園 1年クラブ組 たけし
    
    Attribute:
        favorite_suit (Suit): クラブの使い手

    Note:
        たけしは、手札公開の際に、マークの情報をくれる
        クラブの使い手
    """
    favorite_suit = Suit.club

    def __init__(self):
        super().__init__(name = "たけし", cpu = True)

    def show_hand(self):
        """Show hand.
        手札を開示する

        Return
            list[Card]: 開示する情報
        """
        return super().show_hand(hint="mark-1")
