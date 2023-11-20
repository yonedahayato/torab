from enum import IntEnum
import random

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
    
    def mark(self):
        """Mark.
        スートのマーク
        """
        if self == Suit.spade:
            return "♠"
        elif self == Suit.heart:
            return "♥"
        elif self == Suit.diamond:
            return "♦"
        elif self == Suit.club:
            return "♣"
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
            self.num = 15
            self.suit = None
        elif joker == 2:
            self.num = 14
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
            return f"{self.num} {self.suit.mark()}"
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
    
class Deck(BasePicture):
    """A deck of Nap.
    
    デッキを管理するクラス
    
    Attributes:
        cards (list[Card]): カード
    """
    
    cards = []

    def __init__(self):
        """Constructor.
        
        Note:
            デッキは、数字とスートを持つ52枚のカードとジョーカー2枚からなる、計54枚のカードからなる
        """
        self.cards = [Card(num, suit) for num in range(1, 14) for suit in Suit] + [Card(joker=1), Card(joker=2)]
        print(f"{len(self.cards)} 枚のカードを使用します\n")

    def __len__(self):
        """Length.
        デッキの枚数
        """
        return len(self.cards)
    
    def shuffle(self):
        """Shuffle a deck.
        """
        random.shuffle(self.cards)
        
    def deal(self, num: int = 10):
        """Deal a card.
        
        Args:
            num (int): Number of cards to deal.
            
        Returns:
            list[Card]: Dealed cards.
            
        Exceptions:
            IndexError: If there is no card in a deck.
        """
        try:
            return [self.cards.pop() for _ in range(num)]
        except IndexError:
            print("デッキにカードがありません")
            return []

class Field(BasePicture):
    """A field of Nap.
    
    ゲームのフィールドを管理するクラス
    
    Attributes:
        widow (list): ウィドー
        cards (dict): プレイヤーが出したカード
        trash (list): 捨て札
        trump (Suit): 切り札
    
    Note:
        フィールには、以下の要素がある
        1. ウィドー (widow)
        2. プレイヤーが出したカード (cards)
        3. 出し終わったカード (trash)
        4. 切り札 (trump)
            切り札とは、ナポレオンが宣言した強いスートのこと
    """
    widow = []
    cards = {}
    trash = []
    cards = {}

    # 描画のための設定
    color = "green"
    image_size = [100, 150]

    def set_trump(self, trump: Suit):
        """Set a trump.
        """
        self.trump = trump

    def set_widow(self, widow: list[Card]):
        """Set a widow.
        """
        self.widow = widow
        
    def put_card(self, name: str, card: Card):
        """Put a card.
        
        プレイヤーがカードを出す
        
        Args:
            name (str): Name of a player.
            card (Card): A card.
        """
        self.cards[name] = card
        
    @property
    def lead(self):
        """台札
        一番最初に出されたカードのスート
        """
        return list(self.cards.values())[0].suit
    
    def suit_strength(self, suit: Suit):
        """Suit strength.
        スートの強さを計算する
        
        Note:
            勝者を決める際に、スートの強さを考慮する必要がある
            スートの強さの順番は、以下の通り
            1. 切り札
            2. 台札
            3. spade
            4. heart
            5. diamond
            6. club
        """
        
        if suit == self.trump:
            return 6
        elif suit == self.lead:
            return 5
        elif suit == Suit.spade:
            return 4
        elif suit == Suit.heart:
            return 3
        elif suit == Suit.diamond:
            return 2
        elif suit == Suit.club:
            return 1
        else:
            """
            Note:
                Joker の場合
            """
            return 0

    def show(self):
        """Show a field.
        """
        print(f"ウィドー: {[str(c) for c in self.widow]}")
        print(f"場: {[name + ' : ' + str(c) for name, c in self.cards.items()]}")
        print(f"捨て札: {[str(c) for c in self.trash]}")
        
    def clear(self):
        """Reset a field.
        
        場のカードをリセットする
        """
        self.trash.extend(self.cards.values())
        self.cards = {}