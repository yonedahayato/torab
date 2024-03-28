from PIL import Image

from .player import Player

from .utils.card import (
    Card,
    Suit,
    Deck,
)
from .utils.base import BasePicture

class Field(BasePicture):
    """A field of Nap.
    
    ゲームのフィールドを管理するクラス
    
    Attributes:
        widow (list[Card]): ウィドー
        cards (dict{Player: Card}): プレイヤーが出したカード
        trash (list[Card]): 捨て札
        trump (Suit): 切り札
        
        描画のための設定
        color (str): 背景色
        image_size (list[int]): 画像サイズ
    
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
    trump = None

    color = "green"
    image_size = [150, 100]
    
    def __init__(self, deck: Deck, players: list[Player]):
        """
        Args:
            deck (Deck): xxx
            
        Note:
            カードとプレイヤーがいなければ、そこはフィールドではない
        """
        super().__init__()
        self.deck = deck

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
    
    def suit_strength(self, suit: Suit) -> int:
        """Suit strength.
        スートの強さを計算する
        
        Args:
            suit (Suit): スート
            
        Returns:
            int: スートの強さ

        Note:
            勝者を決める際に、スートの強さを考慮する必要がある

            スートの強さの順番は、以下の通り
            1. 切り札
            2. 台札
            3. spade
            4. heart
            5. diamond
            6. club
            
            ゲームによっては変わるので、コールバックするメソッドをもらって、実行するでもいいかも
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

    def __str__(self, width: int = 50, pad_str: str = "#") -> str:
        """Show a field.
        
        Args:
            width (int): 文字列で表現するときの幅
            pad_str (str): 文字列で表現するときに埋める文字列

        Returns:
            str: フィールドの状況
        """

        field_str = "\n"
        field_str += pad_str * width
        field_str += f"\n{pad_str}\n"

        if len(self.widow) != 0:
            field_str += f"{pad_str}\t\tウィドー: {len(self.widow)}\n"
        field_str += f"{pad_str}\t\t山札: {len(self.deck)}\n"
        field_str += f"{pad_str}\t\t場: {len(self.cards)}\n"
        field_str += f"{pad_str}\t\t捨て札: {len(self.trash)}\n"

        field_str += f"{pad_str}\n"
        field_str += pad_str * width

        return field_str

    def clear(self) -> None:
        """Reset a field.
        
        場のカードをリセットする
        """
        self.trash.extend(self.cards.values())
        self.cards = {}
        
    def make_image(self, save_path: str = None) -> None:
        """
        フィールドを画像として作成する
        
        Args:
            save_path (str): 画像ファイルとして出力するパス
        """
        image = Image.new("RGB", self.image_size, self.color)
        
        if save_path:
            image.save(save_path, quality=95)