from enum import IntEnum

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

class Card:
    """Card class.
    カードクラス

    Attributes:
        num (int): カードの数字
        suit (Suit): カードのスート
    """
    def __init__(self, num: int = 2, suit: Suit = Suit.club) -> None:
        """Constructor.
        
        Args:
            num (int): カードの数字
            suit (Suit): カードのスート
        """
        self.num = num
        self.suit = suit

    def __eq__(self, other):
        """Equal.
        カードの強さが同じかどうか
        """
        return self.num == other.num and self.suit == other.suit
    
    def __gt__(self, other):
        """Greater than.
        カードの強さが他の宣言より強いかどうか
        """
        return self.num > other.num or (self.num == other.num and self.suit > other.suit)
    
    def __ge__(self, other):
        """Greater than or equal.
        カードの強さが他の宣言以上かどうか
        """
        return self.num > other.num or (self.num == other.num and self.suit >= other.suit)
    
    def __lt__(self, other):
        """Less than.
        カードの強さが他の宣言より弱いかどうか
        """
        return self.num < other.num or (self.num == other.num and self.suit < other.suit)
    
    def __le__(self, other):
        """Less than or equal.
        カードの強さが他の宣言以下かどうか
        """
        return self.num < other.num or (self.num == other.num and self.suit <= other.suit)