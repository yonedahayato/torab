from utils import Suit

class Declear:
    """Declear class.
    宣言クラス
    """
    def __init__(self, num: int = 13, suit: Suit = Suit.club) -> None:
        """Constructor.
        
        宣言ができるのは、13 以上の数字のみ
        
        Args:
            num (int): カードの数字
            suit (Suit): カードのスート
        """
        if num < 13:
            raise ValueError("宣言ができるのは、13 以上の数字のみ")

        self.num = num
        self.suit = suit

    def __eq__(self, other):
        """Equal.
        宣言の強さが同じかどうか
        """
        return self.num == other.num and self.suit == other.suit
    
    def __gt__(self, other):
        """Greater than.
        宣言の強さが他の宣言より強いかどうか
        """
        return self.num > other.num or (self.num == other.num and self.suit > other.suit)
    
    def __ge__(self, other):
        """Greater than or equal.
        宣言の強さが他の宣言以上かどうか
        """
        return self.num > other.num or (self.num == other.num and self.suit >= other.suit)
    
    def __lt__(self, other):
        """Less than.
        宣言の強さが他の宣言より弱いかどうか
        """
        return self.num < other.num or (self.num == other.num and self.suit < other.suit)
    
    def __le__(self, other):
        """Less than or equal.
        宣言の強さが他の宣言以下かどうか
        """
        return self.num < other.num or (self.num == other.num and self.suit <= other.suit)

class Player:
    """Player class.
    プレイヤークラス

    Attributes:
        is_nap (bool): ナポレオンかどうか
        is_adjutant (bool): 副官かどうか
        is_allied (bool): 連合軍かどうか
    """

    is_nap = False
    is_adjutant = False
    is_allied = False

    def __init__(self):
        """Constructor.
        """

        self.cards = []

    def take_hand(self, cards):
        """Take hand.
        Args:
            cards (list): List of cards.
        """
        self.cards = cards

    def declare(self, before_declare: Declear = None) -> Declear:
        """Declare.
        宣言する
        
        Args:
            before_declare (Declear): 前の宣言

        Returns:
            Declear: 宣言
            
        Raises:
            ValueError: 宣言が弱い
        """
        declear = Declear()

        if before_declare is None:
            return declear

        if declear <= before_declare:
            raise ValueError("宣言が弱いです")

        return declear