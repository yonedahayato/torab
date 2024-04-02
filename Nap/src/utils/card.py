from enum import IntEnum

from .base import BasePicture

class Suit(IntEnum):
    """Suit class.
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

    @property
    def mark(self) -> str:
        """
        スートのマークを出力する.
        
        Returns:
            str: マークの文字
        """
        self.set_info()
        return self.__mark
    
    @mark.setter
    def mark(self, value) -> None:
        """
        スートのマークを格納する.
        
        Args:
            value: マークの情報
        """
        self.__mark = value
    
    @property
    def image_url(self) -> str:
        """
        スートの画像のURLを出力する
        """
        
        return self.__image_url
    
    @image_url.setter
    def image_url(self, value):
        """
        スートの画像のURLを格納する
        """
        
        self.__image_url = value

    def set_info(self) -> None:
        """
        スートに応じて情報を取得する

        Raises:
            ValueError: マークが異常の場合
        """
        if self == Suit.spade:
            self.mark = "♠"
            self.image_url = "https://docs.google.com/drawings/d/e/2PACX-1vShkEbM-bF8ZdFUUVDTsFPtamISa-TgR2_v26Bzf6f-ugqmt3Ry8Ncj59t3TIEK_Lumr4OoH5WSr7lG/pub?w=596&h=596"
        elif self == Suit.heart:
            self.mark = "♥"
            self.image_url = "https://docs.google.com/drawings/d/e/2PACX-1vS4Y024nBwRGYfrQkJsvh0bsQhNiM8g-_-DMSY_tNslQ6b5noqpYZrQ2fnTQJ7bZiLhXjObDzGGJ1gk/pub?w=596&h=596"
        elif self == Suit.diamond:
            self.mark = "♦"
            self.image_url = "https://docs.google.com/drawings/d/e/2PACX-1vQWHrseqkqz3Yb2On0NewQYzXvtNDxx99aKRHUw36S8XUn2AZ5hhohswUfiQH2bO18CzdF2gVJb_kPw/pub?w=596&h=596"
        elif self == Suit.club:
            self.mark = "♣"
            self.image_url = "https://docs.google.com/drawings/d/e/2PACX-1vRhDX5xCJqqutdXbcfSZxunVzpktaaXClS-0245bLmYFYA5QyDqPyjMfhUFNW73h26kai7TJbAlRRsl/pub?w=596&h=596"
        else:
            raise ValueError("スートが不正です")

class Card(BasePicture):
    """Card class.
    カードクラス
    スートの比較はしない

    Attributes:
        num (int): カードの数字
        suit (Suit): カードのスート
        joer (int): ジョーカーかどうか
        image_url (str): カードの画像のURL
        
    Note:
        カードの種類は、以下の通り
        1. 数字とスートを持つ通常のカード : 52枚
        2. ジョーカー / joker
            a. 強いジョーカー : 1枚
            b. 弱いジョーカー : 1枚
    """

    def __init__(self, num: int = 2, suit: Suit = Suit.club, joker: int = 0) -> None:
        """Constructor.
        
        Args:
            num (int): カードの数字
            suit (Suit): カードのスート
            joker (int): ジョーカーかどうか
                0: 通常のカード
                1: 強いジョーカー
                2: 弱いジョーカー
        """

        if joker == 0:
            self.num = num
            self.suit = suit
        elif joker == 1:
            self.num = 16
            self.suit = None
        elif joker == 2:
            self.num = 15
            self.suit = None
        else:
            raise ValueError("ジョーカーの種類が不正です")
        self.joker = joker
        
        self.set_url()

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
        if self.joker == 0:
            return f"{self.num} {self.suit.mark}"
        elif self.joker == 1:
            return "Joker (strong)"
        elif self.joker == 2:
            return "Joker (weak)"
        
    def set_url(self) -> str:
        """Set a url.
        カードの画像のURLを設定する
        
        Returns:
            str: カードの画像のURL
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
        
        return self.image_url