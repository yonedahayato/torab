from ..utils import (
    Suit,
    Card,
    Deck,
    SimpleDeck,
)

from ..field import (
    Field,
)

from ..player import (
    Takeshi,
    Player,
)

from .track import (
    Track,
    SimpleTrack,
    NapTrack,
)

class Game:
    """A game of Nap.
    
    ゲームの進行を管理するクラス
    複数の Track を行う
    
    Attributes:
        hand_num (int): Number of cards to deal to each player.
        
        field (Field): ゲームを行うためのフィールド
    """
    hand_num = 10

    def __init__(self):
        """
        Note:
            ゲームのための準備
                1. フィールドの設営
                    a. カードを準備する
                    b. プレイヤーを着席させる
                2. カードをシャフル
                3. カードを配る
                4. Track を準備
        """
        deck = self.set_deck()
        players = self.set_player()

        self.field = Field(deck, players)
        self.shuffle()
        self.deal()
        self.set_track(start_player_id=0)
        print(self.field)
        
    def set_deck(self) -> Deck:
        """
        ゲームに利用するカードを準備する
        """
        deck = Deck()
        return deck

    def set_player(self) -> list[Player]:
        """
        ゲームに参加させるプレイヤーを着席させる
        
        Returns:
            list[Player]: ゲームに参加するプレイヤー
        """
        return [Player("Boss", cpu=True), Player("You", cpu=False)]

    def shuffle(self) -> None:
        """Shuffle a deck.
        
        そのゲームにおけるシャッフル方法でシャッフルする
        """
        self.field.deck.shuffle()

    def deal(self) -> None:
        """Deal cards.

        カードを各プレイヤーに配る
        """
        for player in self.field.players:
            player.take_hand(self.field.deck.deal(self.hand_num))
    
    def set_track(self, start_player_id: int):
        """
        
        ゲームで利用する Tack を設定する
        
        Args:
            start_player_id (int): この Track で最初にプレイするプレイヤーの index
        """
        self.track = SimpleTrack(
                        field = self.field, 
                        start_player_id = start_player_id, 
                        trump = Suit.spade)
        
    def decide_winner_in_track(self) -> Player:
        """
        ある Track における勝者を決定する
        """
        
    def add_point(self, player: Player) -> None:
        player.point += 1

    def play(self) -> None:
        """
        トラックの進行を行う
        
        Note:
            ある Track における処理の流れ
                1. 各プレイヤーがカードを出す (track のイテレーション)
                2. その Track における勝者を決める
                3. 勝者にポイントを付与
                3. フィールドの場を綺麗にする
                4. 次の Track の準備
        """
        for track_cnt in range(self.hand_num):
            for field in self.track:
                print(field)
            winner = self.decide_winner_in_track()
            self.add_point(winner)

            print(field)
            self.field.clear()
            self.set_track(start_player_id = 0)
            
        winner = self.decide_winner_in_game()
        field.message = f"このゲームの勝者は、{winner} です"
        print(field)

class SimpleNapGame(Game):
    """
    シンプルなトラックテイキング

    Attributes:
        hand_num (int): このゲームでは、手札は 3 or 5
    """
    hand_num = 3

    def set_deck(self) -> Deck:
        """
        ゲームに利用するカードを準備する
        
        Note:
            ジョーカーのない Deck を利用する
        """
        deck = SimpleDeck()
        return deck

    def calculate_strongness(self, card: Card) -> tuple[int, int]:
        """
        このゲームにおけるそのカードの強さを計算する
        
        Args:
            card (Card): 強さを計算するカード
            
        Returns:
            Tuple[int, int]: 数字の強さ, スートの強さ

        Note:
            切り札のスートの強さ優先
                trump (切り札) > 台札 > spade > heart > diamond > club
            次に、数字の強さ
                A > K > Q > J > 10 > ... > 2
        """

    def decide_winner_in_track(self) -> Player:
        """
        ある Track における勝者を決定する
        
        Returns:
            ある Track における勝者
        """
        cards_power = {name: self.calculate_strongness(card) for name, card in self.field.cards.items()}
        winner_name, card_power = max(cards_power.items(), key=lambda x: (x[1][1], x[1][0]))
        winner_id = list(self.field.cards.keys()).index(winner_name)

        return self.field.players[winner_id]
    
    def decide_winner_in_game(self) -> Player:
        """
        各プレイヤーのポイントから勝者を決定する
        """
        
        return max(self.field.players, key = lambda p: p.point)

class SimpleNapVSTakeshi(SimpleNapGame):
    """
    たけしとのシンプルなトラックテイキングで勝負
    """
    def set_player(self) -> list[Player]:
        return [Takeshi(), Player("You", cpu=False)]

    def deal(self) -> None:
        """Deal cards.

        カードを各プレイヤーに配る
        たけしには、クラブのカードを渡す
        """
        takeshi_hand = [Card(num = n, suit = Suit.club) for n in range(1, 1 + self.hand_num)]

        for player in self.field.players:
            if player.name == "たけし": 
                takeshi_hand = self.field.deck.pull_out(takeshi_hand)
                player.take_hand(takeshi_hand)
            else:
                player.take_hand(self.field.deck.deal(self.hand_num))

    def calculate_strongness(self, card: Card) -> tuple[int, int]:
        """
        このゲームにおけるそのカードの強さを計算する
        
        Args:
            card (Card): 強さを計算するカード
            
        Returns:
            Tuple[int, int]: 数字の強さ, スートの強さ

        Note:
            切り札のスートの強さ優先
                trump (切り札, 6) > spade (4) > heart (3) > diamond (2) > club (1)
                台札のルールはなし
            次に、数字の強さ
                A > K > Q > J > 10 > ... > 2
        """
        if card.num == 1:
            num_power = 14
        else:
            num_power = card.num

        if card.suit == self.field.trump:
            suit_power = 6
        else:
            suit_power = int(card.suit)

        return (num_power, suit_power)

class NapGame(Game):
    """
    ナポレオンのゲームの進行を管理する

    Attributes:
        hand_num (int): Number of cards to deal to each player.
        widow_num (int): Number of cards to deal to widow.
    """
    hand_num = 10
    widow_num = 4

    def __init__(self, field: Field):
        """Constructor.
        Note:
            ゲームの流れ
                1. デッキをシャッフルする
                2. デッキからカードを配る
                3. プレイヤーが強さを宣言する
                    a. この宣言にて、ナポレオンが決まる
                    b. ナポレオンが宣言したスートが切り札となる
                4. Track を 10回行う
                    a. プレイヤーがカードを出す
                    b. 出されたカードの強さを比較する
                    c. 強いカードを出したプレイヤーが勝ち
                5. プレイヤーの勝敗を決める
        """
        self.field = field
        
    def deal(self):
        """Deal cards.
        カードを各プレイヤーに配る
        あまったカードはウィドーに置く
        """
        for player in self.field.players:
            player.take_hand(self.field.deck.deal(self.hand_num))

        self.field.widow = self.field.deck.deal(self.widow_num)

    def declare(self):
        """Declare a strength.
        自身のカードの強さを宣言する
        
        Note:
            1. 最初(親)のプレイヤーから宣言する
            2. 次のプレイヤーは前の宣言より強い宣言をする、またはパスする
            3. パスをしたら、そのプレイヤーは宣言できなくなる
            4. 全員パスしたら、ウィドーのカードを1枚公開し、そのカードのスートのJを持つプレイヤーがナポレオン
        """
        while True:
            strong_declear = None
            for player in self.players:
                declear = player.declare(strong_declear)

                if declear <= strong_declear:
                    pass
                else:
                    pass
                strong_declear = declear

    def play(self):
        """Play a game.
        """
        for _ in range(10):
            track = Track(self.deck, self.players, self.field)
            track.play()
            self.field.clear()
