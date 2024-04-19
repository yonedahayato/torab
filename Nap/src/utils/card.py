from enum import IntEnum
from pydantic import BaseModel, Field

from .base import BasePicture

class Suit(IntEnum):
    """
    スートクラス

    Note:
        カードのスートの強さ
        1. スペード / spade
        2. ハート / heart
        3. ダイヤ / diamond
        4. クラブ / club
    """
    spade = 4
    heart = 3
    diamond = 2
    club = 1

    def __init__(self, value: int):
        self._value_ = value
        self._set_info(value)

    @property
    def mark(self) -> str:
        """
        スートのマークを出力する.
        
        Returns:
            str: マークの文字
        """
        return self.__mark
    
    @property
    def image_url(self) -> str:
        """
        スートの画像のURLを出力する
        
        Returns:
            str: スートの画像のURL
        """
        
        return self.__image_url

    def _set_info(self, value: int) -> None:
        """
        スートに応じて情報を取得する
        
        Args:
            value (int): IntEnum class の値

        Raises:
            ValueError: マークが異常の場合
            
        Note:
            URL は、このプロジェクトのために作成したスートの画像
        """
        if value == 4:
            self.__mark = "♠"
            self.__image_url = "https://docs.google.com/drawings/d/e/2PACX-1vShkEbM-bF8ZdFUUVDTsFPtamISa-TgR2_v26Bzf6f-ugqmt3Ry8Ncj59t3TIEK_Lumr4OoH5WSr7lG/pub?w=596&h=596"
        elif value == 3:
            self.__mark = "♥"
            self.__image_url = "https://docs.google.com/drawings/d/e/2PACX-1vS4Y024nBwRGYfrQkJsvh0bsQhNiM8g-_-DMSY_tNslQ6b5noqpYZrQ2fnTQJ7bZiLhXjObDzGGJ1gk/pub?w=596&h=596"
        elif value == 2:
            self.__mark = "♦"
            self.__image_url = "https://docs.google.com/drawings/d/e/2PACX-1vQWHrseqkqz3Yb2On0NewQYzXvtNDxx99aKRHUw36S8XUn2AZ5hhohswUfiQH2bO18CzdF2gVJb_kPw/pub?w=596&h=596"
        elif value == 1:
            self.__mark = "♣"
            self.__image_url = "https://docs.google.com/drawings/d/e/2PACX-1vRhDX5xCJqqutdXbcfSZxunVzpktaaXClS-0245bLmYFYA5QyDqPyjMfhUFNW73h26kai7TJbAlRRsl/pub?w=596&h=596"
        else:
            raise ValueError("スートが不正です")

class Card(BaseModel, BasePicture):
    """
    カードクラス
    スートの比較はしない

    Attributes:
        num (int): カードの数字
            1 ~ 13, 15, 16
        suit (Suit): カードのスート
        joer (int): ジョーカーかどうか
            0, 1, 2
        image_url (str): カードの画像のURL

    Note:
        カードの種類は、以下の通り
        1. 数字とスートを持つ通常のカード : 52枚
        2. ジョーカー / joker
            a. 強いジョーカー : 1枚
            b. 弱いジョーカー : 1枚
    """
    num: int = Field(default = 2, ge = 1, le = 16)
    suit: Suit | None = Suit.club
    joker: int = Field(default = 0, ge = 0, le = 2)
    image_url: str | None = None

    def __init__(self, num: int = 2, suit: Suit = Suit.club, joker: int = 0):
        """

        Args:
            num (int): カードの数字
            suit (Suit): カードのスート
            joker (int): ジョーカーかどうか
                0: 通常のカード
                1: 強いジョーカー
                2: 弱いジョーカー
                
        Raises:
            ValueError: 数字の数が異常
            ValueError: ジョーカーの種類が不正です
        """

        if joker == 0:
            if int(num) > 13:
                raise ValueError("数字の数が異常")
        elif joker == 1:
            num = 16
            suit = None
        elif joker == 2:
            num = 15
            suit = None
        
        super().__init__(num = num, suit = suit, joker = joker)
        self._set_url()

    def __eq__(self, other) -> bool:
        """Equal.
        カードの強さが同じかどうか
        
        """
        return self.num == other.num
    
    def __gt__(self, other) -> bool:
        """Greater than.
        カードの強さが他のカードより強いかどうか
        """
        return self.num > other.num
    
    def __ge__(self, other) -> bool:
        """Greater than or equal.
        カードの強さが他のカード以上かどうか
        """
        return self.num >= other.num
    
    def __lt__(self, other) -> bool:
        """Less than.
        カードの強さが他のカードより弱いかどうか
        """
        return self.num < other.num
    
    def __le__(self, other) -> bool:
        """Less than or equal.
        カードの強さが他のカード以下かどうか
        """
        return self.num <= other.num
    
    def __str__(self) -> str:
        """String.
        カードの文字列表現
        """
        if str(self.num) == "1":
            num = "A"
        elif str(self.num) == "13":
            num = "K"
        elif str(self.num) == "12":
            num = "Q"
        elif str(self.num) == "11":
            num = "J"
        else:
            num = self.num

        if self.joker == 0:
            return f"{self.suit.mark}-{num}"
        elif self.joker == 1:
            return "Joker (strong)"
        elif self.joker == 2:
            return "Joker (weak)"
        
    def _set_url(self):
        """
        カードの画像のURLを設定する
        
        Attributes:
            image_url (str): カードの画像のURL
        """

        if self.joker == 1:
            self.image_url = "https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust53.png"            
        elif self.joker == 2:
            self.image_url = "https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust54.png"            
        elif self.suit == Suit.spade:
            self.image_url = f"https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust{self.num}.png"
        elif self.suit == Suit.club:
            self.image_url = f"https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust{self.num + 13}.png"
        elif self.suit == Suit.diamond:
            self.image_url = f"https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust{self.num + (13 * 2)}.png"
        elif self.suit == Suit.heart:
            self.image_url = f"https://chicodeza.com/wordpress/wp-content/uploads/torannpu-illust{self.num + (13 * 3)}.png"
        else:
            raise ValueError("カードの種類が不正です")
        
    def is_joker(self) -> bool:
        """
        このカードがジョーカーかどうかを出力する
        
        Returns:
            bool : このカードがジョーカーかどうか
        """
        return self.joker in [1, 2]