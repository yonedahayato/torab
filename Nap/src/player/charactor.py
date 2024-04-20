import random
from typing import ClassVar

from .player import Player
from ..utils import Suit

class Charactor(Player):
    """
    キャラクターのクラス
    """
    @classmethod
    def talk(self, theme: str):
        """
        キャラクターのセリフを出力する

        Args:
            theme (str): トークテーマ
        """
        raise NotImplementedError

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
        手札を開示する

        Return
            list[Card]: 開示する情報
        """
        return super().show_hand(hint="mark-1")
    
    @classmethod
    def talk(cls, theme: str) -> str:
        """
        話してくれる
        
        Args:
            theme (str): トークテーマ
        """
        if theme in cls.lines.keys():
            lines = cls.lines.get(theme)
        else:
            lines = random.choice(list(dict.values()))
        return lines
