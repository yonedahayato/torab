from .utils import (
    Suit,
    Card,
    Field,
)

import random

class Declear:
    """Declear class.
    宣言クラス
    
    Note:
        宣言は、ナポレオンになりたいプレイヤーが行う
        宣言の強さは、(ゲーム内で獲得できるであろう)枚数と(切り札となる)スートの強さで決まる
        ナポレオンになりたくないプレイヤーは、宣言を行わない (pass を宣言する)
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
        
    Note:
        プレイヤーは、ナポレオン、副官、連合軍のいずれかである

        プレイヤーが行うことができることは、以下の通り
            1. 手札を受け取る
            2. 宣言する
            3. カードを出す
        
        CPU は、ランダムに宣言する
    """

    is_nap = False
    is_adjutant = False
    is_allied = False

    def __init__(self, name: str = "Unknown", cpu: bool = False):
        """Constructor.
        
        Args:
            name (str): プレイヤーの名前
            cpu (bool): CPU かどうか
        """

        self.cards = []
        self.name = name
        self.cpu = cpu

    def __str__(self):
        """String.
        """
        return self.name

    def take_hand(self, cards: list[Card]):
        """Take hand.
        Args:
            cards (list): List of cards.
        """
        self.cards = sorted(cards)
        
    def show_hand(self):
        """Show hand.
        手札を表示する
        """
        print({i: str(c)for i, c in enumerate(self.cards)})

    def declare(self, strong_declear: Declear, is_random: bool = False) -> Declear:
        """Declare.
        宣言する
        
        Args:
            strong_declear (Declear): 一番強い宣言
            is_random (bool): ランダムに宣言するかどうか

        Returns:
            Declear: 宣言
            
        Raises:
            ValueError: 宣言が弱い
        """

        if is_random:
            num = random.randint(13, 20)
            suit = random.choice([Suit.spade, Suit.heart, Suit.diamond, Suit.club])
        else:
            num = int(input("宣言する数字を入力してください: "))
            suit = int(input("宣言するスートを入力してください: "))
            
        declear = Declear(num, suit)

        return declear
    
    def play_card(self, field: Field, is_random: bool = False) -> Card:
        """Play card.
        カードを出す
        
        Args:
            field (Field): フィールド
            is_random (bool): ランダムにカードを出すかどうか
            
        Returns:
            Card: カード
        """
        if not self.cpu:
            self.show_hand()
            try:
                card_id = int(input("出すカードを入力してください: "))
            except ValueError:
                raise ValueError("カードの番号を入力してください")
            card = self.cards.pop(card_id)

        elif is_random or self.cpu:
            card = random.choice(self.cards)

        return card