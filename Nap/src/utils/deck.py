import random

from .base import BasePicture
from .card import (
    Suit,
    Card,
)

from .logger import Logger
logger = Logger()
print = logger.log_print

class Deck(BasePicture):
    """
    デッキを管理するクラス    
    """

    def __init__(self):
        """
        Attributes:
            cards (list[Card]): カード

        Note:
            デッキは、数字とスートを持つ52枚のカードとジョーカー2枚からなる、計54枚のカードからなる
        """
        self.cards = [Card(num, suit) for num in range(1, 14) for suit in Suit] + [Card(joker=1), Card(joker=2)]
        print(f"{len(self.cards)} 枚のカードを使用します\n")

    def __len__(self) -> int:
        """
        デッキの枚数
        
        Returns:
            int: 現在のデッキの枚数
        """
        return len(self.cards)

    def __str__(self) -> str:
        """
        デッキの状態を表示
        
        Returns:
            str: デッキの状態
        """
        return str([str(c) for c in self.cards])

    def shuffle(self) -> None:
        """
        デッキをシャッフルする
        """
        random.shuffle(self.cards)
        
    def deal(self, num: int = 10):
        """
        
        特定の枚数のカードを引く
        
        Args:
            num (int): Number of cards to deal.
            
        Returns:
            list[Card]: Dealed cards.
            
        Raises:
            IndexError: If there is no card in a deck.
        """
        try:
            return [self.cards.pop() for _ in range(num)]
        except IndexError:
            print("デッキにカードがありません")
            return []
        
    def pull_out(self, targets: list[Card]) -> list[Card]:
        """
        特定のカードを引き抜く
        
        Args:
            target (list[Card]): 対象のカード

        Returns:
            list[Card]: 山札から削除した対象のカード
            
        Note:
            Card Class の仕様について
                Card Class は少々、特殊な大小関係の計算をする
                そのため、remove method を正直に使えない
                
                そのための対応として、target_id を取得し,
                del 構文で削除する
        """
        deleted_cards = []
        for target_card in targets:
            if str(target_card) not in [str(c) for c in self.cards]:
                raise ValueError("削除するカードがありません")

            target_id = [str(c) for c in self.cards].index(str(target_card))
            del self.cards[target_id]
            deleted_cards.append(target_card)

        return deleted_cards

class SimpleDeck(Deck):
    """
    ジョーカーのないシンプルカードプール

    Attributes:
        cards (list[Card]): カード
    """

    def __init__(self):
        """Constructor.

        Note:
            デッキは、数字とスートを持つ52枚のカードからなる
        """
        self.cards = [Card(num, suit) for num in range(1, 14) for suit in Suit]
        print(f"{len(self.cards)} 枚のカードを使用します\n")