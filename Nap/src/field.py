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
        # 描画のための設定
        color (str): 背景色
        image_size (list[int]): 画像サイズ

        # ゲームに関する変数
        widow (list[Card]): ウィドー
        cards (dict{Player: Card}): プレイヤーが出したカード
        trash (list[Card]): 捨て札
        trump (Suit): 切り札
        
        # その他
        deck (Deck): トランプ
        players (list[Player]): プレイヤー
        message (str): プレイヤーへ情報を提示する際に使用する

    Note:
        フィールには、以下の要素がある
        1. ウィドー (widow)
        2. プレイヤーが出したカード (cards)
        3. 出し終わったカード (trash)
        4. 切り札 (trump)
            切り札とは、ナポレオンが宣言した強いスートのこと
    """

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
        self._widow = []
        self._trump = None
        self.cards = {}
        self.trash = []

        self.deck = deck
        self.players = players
        self._message = ""

    def __str__(self, width: int = 50, pad_str: str = "#") -> str:
        """Show a field.
        
        Args:
            width (int): 文字列で表現するときの幅
            pad_str (str): 文字列で表現するときに埋める文字列

        Returns:
            str: フィールドの状況
            
        Note:
            以下の情報を文字列にて表示

            1. フィールド状況 (カード数)
                a. ウィドー
                b. 山札
                c. 場 (プレイヤーが出したカード)
                d. 捨て札
                e. 切り札情報
                
            2. プレイヤーの情報
                a. 手札の情報
                    プレイヤーにカードを見せてもらう
        """

        token_tab1 = f"{pad_str}\t"
        token_tab2 = f"{pad_str}\t\t"
        token_tab3 = f"{pad_str}\t\t\t"
        token_tab4 = f"{pad_str}\t\t\t\t"

        field_str = "\n"
        field_str += pad_str * width
        field_str += f"\n{pad_str}\n"

        if len(self.widow) != 0:
            field_str += f"{token_tab3}ウィドー: {len(self.widow)}\n"
        field_str += f"{token_tab3}山札: {len(self.deck)}\n"
        field_str += f"{token_tab3}捨て札: {len(self.trash)}\n"
        if len(self.cards) == 0:
            field_str += f"{token_tab3}場: {len(self.cards)}\n"
        else:
            field_str += f"{token_tab3}場:\n"
            for n, c in self.cards.items():
                field_str += f"{token_tab4}{n}: {str(c)}\n"
        if self.trump:
            field_str += f"{token_tab3}切り札: {self.trump.mark}\n"

        field_str += f"{pad_str}\n"
        field_str += f"{token_tab1}Players\n"
        for player in self.players:
            hand = player.show_hand()
            field_str += f"{token_tab2}{player}: {[str(card) for card in hand]}\n"
            
        if self.message != "":
            field_str += f"{pad_str}\n"
            field_str += f"{token_tab1}Message\n"
            field_str += f"{token_tab2}{self.message}\n"
            field_str += f"{pad_str}\n"
            self.message = ""

        field_str += f"{pad_str}\n"
        field_str += pad_str * width

        return field_str

    @property
    def trump(self) -> Suit:
        """切り札の getter
        """
        return self._trump
    
    @trump.setter
    def trump(self, trump: Suit) -> None:
        """切り札の setter
        """
        self._trump = trump

    @property
    def widow(self) -> list[Card]:
        """ウィドーの getter
        """
        return self._widow
    
    @widow.setter
    def widow(self, widow: list[Card]) -> None:
        """ウィドーの setter
        """
        self._widow = widow
    
    @property
    def message(self):
        """メッセージの getter
        """
        return self._message
    
    @message.setter
    def message(self, message) -> None:
        """メッセージの setter
        """
        self._message = message

    @property
    def lead(self) -> Suit:
        """台札
        一番最初に出されたカードのスート
        """
        return list(self.cards.values())[0].suit

    def put_card(self, name: str, card: Card):
        """Put a card.
        
        プレイヤーのカードを受け取る
        
        Args:
            name (str): Name of a player.
            card (Card): A card.
        """
        self.cards[name] = card
    
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