import random
from typing import ClassVar

from .player import Player
from ..utils import Suit

class Charactor(Player):
    """
    キャラクターのクラス
    """
    @classmethod
    def talk(cls, theme: str) -> str:
        """
        キャラクターのセリフを出力する
        
        Args:
            theme (str): トークテーマ
        """
        if theme in cls.lines.keys():
            lines = cls.lines.get(theme)
        else:
            lines = random.choice(list(dict.values()))
        return lines

class Takeshi(Charactor):
    """
    トランプ学園 1年クラブ組 たけし
    
    Attribute:
        favorite_suit (Suit): クラブの使い手
        lines (dict{str: str}): セリフ

    Note:
        三井たけし
        たけしは、手札公開の際に、マークの情報をくれる
        クラブの使い手
    """
    favorite_suit: ClassVar[Suit] = Suit.club
    lines: ClassVar[dict[str, str]] = {
        "introduction": "俺の名前は、たけし！",
        "favorite": "好きなスートは、クラブさ！",
        "rule": "ハンデとして手札のスートを一枚だけ教えてやるよ！",
        "conversation_1": "むむむ！",
        "conversation_2": "お前！やるな！",
    }

    def __init__(self):
        super().__init__(name = "たけし", cpu = True)

    def show_hand(self):
        """Show hand.
        このキャラクターが持つハンデ
        手札を開示する

        Return
            list[Card]: 開示する情報
        """
        return super().show_hand(hint="mark-1")

class Shizuka(Charactor):
    """
    トランプ学園 1年ハート組 しずか
    
    Attribute:
        favorite_suit (Suit): ハートの使い手
        lines (dict{str: str}): セリフ

    Note:
        愛川しずか
        しずかは、手札公開の際に、数字の情報をくれる
        ハートの使い手
    """
    favorite_suit: ClassVar[Suit] = Suit.heart
    lines: ClassVar[dict[str, str]] = {
        "introduction": "私の名前は、しずか！",
        "favorite": "好きなスートは、ハート！",
        "rule": "ハンデとして手札の数字を一枚だけ教える",
        "conversation_1": "なるほど！",
        "conversation_2": "君！なかなかね！",
    }

    def __init__(self):
        super().__init__(name = "しずか", cpu = True)

    def show_hand(self):
        """Show hand.
        このキャラクターが持つハンデ
        手札を開示する

        Return
            list[Card]: 開示する情報
        """
        return super().show_hand(hint="num-1")