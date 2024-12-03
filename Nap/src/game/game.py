from time import sleep
import random

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

from ..bid import (
    NapBid,
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
        time_lag (int): Track の設定
    """
    hand_num = 10
    time_lag = 0

    def __init__(self, 
                 player_how_to_choose: str = "input", 
                 first_message: str = None):
        """
        Args:
            player_how_to_choose (str): CPU でないプレイヤーがどのようにカードを選択するか
                Player class 参照
            first_message (str): フィールドに最初に表示させるメッセージ

        Attributes:
            field (Field): ゲームを行うためのフィールド

        Note:
            ゲームのための準備
                1. フィールドの設営
                    a. カードを準備する
                    b. プレイヤーを着席させる
                2. カードをシャフル
                3. カードを配る
                4. 切り札の決定
                5. Track を準備
        """
        deck = self.set_deck()
        players = self._set_player(player_how_to_choose)
        self.field = Field(deck, players)

        self.shuffle()
        self.deal()
        self._set_trump()
        self.track_cnt = 0
        self.set_track(start_player_id = 0)

        if first_message:
            self.field.message = first_message
        print(self.field)
        sleep(self.time_lag)
        
    def set_deck(self) -> Deck:
        """
        ゲームに利用するカードを準備する
        """
        deck = Deck()
        return deck

    def _set_player(self, how_to_choose: str = "input") -> list[Player]:
        """
        ゲームに参加させるプレイヤーを着席させる

        Args:
            how_to_choose (str): CPU でないプレイヤーがどのようにカードを選択するか
                Player class 参照

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
    
    def _set_trump(self):
        """
        切り札を決定する
        """
        raise NotImplementedError
    
    def get_start_player_id(self) -> int:
        """
        次のトラックを始めるべきプレイヤーの id を取得する
        
        Returns:
            int: 次のトラックを始めるべきプレイヤーの id
            
        Note:
            常にたけしが先行
        """
        return 0

    def set_track(self, start_player_id: int = 0):
        """
        
        ゲームで利用する Tack を設定する
        
        Args:
            start_player_id (int): この Track で最初にプレイするプレイヤーの index
        """
        self.track = SimpleTrack(
                        field = self.field, 
                        start_player_id = start_player_id, 
                        time_lag = self.time_lag)

    def decide_winner_in_track(self) -> Player:
        """
        ある Track における勝者を決定する
        """
        raise NotImplementedError

    def add_point(self, player: Player) -> None:
        """
        そのゲームにおける得点の方法に従い、プレイヤーに得点を与える
        """
        player.point += 1

    def close_track(self) -> None:
        """
        トラックの終了処理
        """
        winner = self.decide_winner_in_track()
        self.add_point(winner)

        self.field.message = f"Track {self.track_cnt+1} を {winner} がとりました"
        print(self.field)

    def next_track(self) -> None:
        """
        新しいトラックの準備
        """
        # 場のカードをリセット
        self.field.clear()

        self.track_cnt += 1
        start_player_id = self.get_start_player_id()
        self.set_track(start_player_id = start_player_id)

        self.field.message = "次の Track です"
        print(self.field)

    def close_game(self) -> None:
        """
        ゲームを終了させる
        """
        winner = self.decide_winner_in_game()
        self.field.message = f"このゲームの勝者は、{winner} です"
        print(self.field)

    def play(self) -> None:
        """
        トラックの進行を行う
        
        Note:
            a. 手札の枚数分、track を行う

            b. ある Track における処理の流れ
                1. 各プレイヤーがカードを出す (track のイテレーション)
                2. その Track における勝者を決める
                3. 勝者にポイントを付与
                3. フィールドの場を綺麗にする
                4. 次の Track の準備
                    
            c. ゲームにおける勝者を決定する
        """
        for track_cnt in range(self.hand_num):
            for field in self.track:
                print(field)

            self.field = field

            # トラックの終わりの処理
            self.close_track()

            # 次のトラックの準備
            self.next_track()

        self.close_game()

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

    def _set_trump(self):
        """
        切り札を設定する

        Note:
            切り札は、スペードで固定

        """
        self.field.trump = Suit.spade

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
    
    def decide_winner_in_track(self) -> Player:
        """
        ある Track における勝者を決定する
        
        Returns:
            ある Track における勝者
        """
        cards_power = {name: self.calculate_strongness(card) for name, card in self.field.cards.items()}
        winner_name, card_power = max(cards_power.items(), key=lambda x: (x[1][1], x[1][0]))
        winner_id = [player.name for player in self.field.players].index(winner_name)
        self.winner_id_in_track = winner_id

        return self.field.players[winner_id]
    
    def decide_winner_in_game(self) -> Player:
        """
        各プレイヤーのポイントから勝者を決定する

        Note:
            ポイントが同点であった場合、プレイ順が早い方が優先的に勝利となる
        """
        
        return max(self.field.players, key = lambda p: p.point)

class EasyNapGame(SimpleNapGame):
    """
    SimpleNapGame の難易度を標準化
    
    Attributes:
        decribe (str): ゲームの説明
        hand (int): 手札の枚数
    """
    describe = \
"""
- 手札は 5 枚 (5 トリックの勝負)
- 台札あり (スートの請求もあり)
- 切り札は、ランダム
- 最初のトリックの先行は、ランダム / その後は前のトリックの勝者
- ジョーカーなしの 52 枚のカード
"""
    hand_num = 5

    def __init__(self, 
                 player_how_to_choose: str = "input", 
                 first_message: str = None):
        """
        Args:
            player_how_to_choose (str): CPU でないプレイヤーがどのようにカードを選択するか
                Player class 参照
            first_message (str): フィールに最初に表示させるメッセージ
        """
        super().__init__(player_how_to_choose, first_message)
        self.field.is_use_lead = True

    def _set_trump(self):
        """
        切り札を設定する

        Note:
            切り札は、ランダム

        """
        self.field.trump = [Suit.spade, Suit.heart, Suit.diamond, Suit.club][random.randint(0, 3)]

    def get_start_player_id(self) -> int:
        """
        次のトラックを始めるべきプレイヤーの id を取得する
        
        Returns:
            int: 次のトラックを始めるべきプレイヤーの id

        Note:
            最初のトリックの先行は、ランダム / その後は前のトリックの勝者
        """
        if self.track_cnt == 0:
            start_player_id = random.randint(0, len(self.field.players)-1)

        else:
            start_player_id = self.winner_id_in_track

        return start_player_id

    def set_track(self, start_player_id: int = None):
        """
        
        ゲームで利用する Tack を設定する
        
        Args:
            start_player_id (int): この Track で最初にプレイするプレイヤーの index

        Note:
            最初のトラックは、ランダム
            次の Track を始めるプレイヤーは、前の Track の勝者            
        """
        self.track = Track(
                        field = self.field, 
                        start_player_id = start_player_id, 
                        time_lag = self.time_lag)

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
        if card.num == 1:
            num_power = 14
        else:
            num_power = card.num

        if card.suit == self.field.trump:
            suit_power = 6
        elif card.suit == self.field.lead:
            suit_power = 5
        else:
            suit_power = int(card.suit)

        return (num_power, suit_power)

class NapGame(EasyNapGame):
    """
    ナップのゲームの進行を管理する

    Attributes:
        decribe (str): ゲームの説明
        hand (int): 手札の枚数
    """
    describe = \
"""
- 手札は 5 枚 (5 トリックの勝負)
- ビットを行いデクレアラーを決定する
- 台札あり (スートの請求もあり)
- 切り札は、最初のトラックのリードのスート
- 最初のトリックの先行は、デクレアラー / その後は前のトリックの勝者
- ジョーカーなしの 52 枚のカード
"""
    hand_num = 5

    def __init__(self, 
                 player_how_to_choose: str = "input", 
                 first_message: str = None):
        """
        Args:
            player_how_to_choose (str): CPU でないプレイヤーがどのようにカードを選択するか
                Player class 参照
            first_message (str): フィールドに最初に表示させるメッセージ

        Attributes:
            field (Field): ゲームを行うためのフィールド

        Note:
            ゲームのための準備
                1. フィールドの設営
                    a. カードを準備する
                    b. プレイヤーを着席させる
                2. カードをシャフル
                3. カードを配る
                4. Bid の準備
        """
        deck = self.set_deck()
        players = self._set_player(player_how_to_choose)
        self.field = Field(deck, players)
        self.shuffle()
        self.deal()
        self.bid_manager = NapBid(self.field)
        self.track_cnt = 0

        if first_message:
            self.field.message = first_message
        print(self.field)
        sleep(self.time_lag)
        # super().__init__(player_how_to_choose, first_message)
        self.field.is_use_lead = True

    def _set_trump(self, suit: Suit):
        """
        切り札を決定する

        Note:
            切り札は、最初のトラックのリードのスート
        """
        self.field.trump = suit

    def get_start_player_id(self) -> int:
        """
        次のトラックを始めるべきプレイヤーの id を取得する
        
        Returns:
            int: 次のトラックを始めるべきプレイヤーの id

        Note:
            最初のトリックの先行は、ティクレアラー / その後は前のトリックの勝者
        """
        if self.track_cnt == 0:
            start_player_id = self.field.players.index(self.bid_manager.declarer)

        else:
            start_player_id = self.winner_id_in_track

        return start_player_id

    def decide_winner_in_game(self) -> Player:
        """
        各プレイヤーのポイントから勝者を決定する

        Note:
            ディクレアラーが宣言を達成できたかどうか
        """
        declarer_id = self.field.players.index(self.bid_manager.declarer)
        declarer_point = self.field.players[declarer_id].point
        is_achived = self.bid_manager.best_declaration.is_achieved(declarer_point)
        game_point = self.bid_manager.best_declaration.get_point(is_achieved=is_achived)

        if is_achived:
            result_text = "成功"
        else:
            result_text = "失敗"

        self.field.message = f"{self.bid_manager.declarer} の {str(self.bid_manager.best_declaration)} は {result_text}し、{game_point} 点獲得です"
        print(self.field)

    def bid(self):
        """
        ビッドを実行し、完了したら、track を始める準備を行う
        """
        for field in self.bid_manager:
            print(field)

        self.field = field
        self.close_bid()

    def close_bid(self):

        if self.bid_manager.invalid:
            raise Exception("この試合は無効")

        self.declarer = self.bid_manager.declarer
        self.best_declaration = self.bid_manager.best_declaration

        self.field.declaration = str(self.bid_manager.best_declaration)
        self.field.declarer = str(self.bid_manager.declarer)
        self.field.message = f"{self.bid_manager.declarer} の {str(self.bid_manager.best_declaration)} が有効です"
        print(self.field)

        # start_player_id = self.field.players.index(self.bid_manager.declarer)
        start_player_id = self.get_start_player_id()
        self.set_track(start_player_id = start_player_id)

    def play(self) -> None:
        """
        ゲームの進行を行う
        
        Note:
            a. 手札の枚数分、track を行う

            b. ある Track における処理の流れ
                1. 各プレイヤーがカードを出す (track のイテレーション)
                    最初の Track のリードで、切り札が決定
                2. その Track における勝者を決める
                3. 勝者にポイントを付与
                3. フィールドの場を綺麗にする
                4. 次の Track の準備
                    
            c. ゲームにおける勝者を決定する
        """
        for track_cnt in range(self.hand_num):
            for take_cnt, field in enumerate(self.track):
                if take_cnt == 0 and track_cnt == 0:
                    card = self.field.cards[self.bid_manager.declarer]
                    #切り札は、最初のトラックのリードのスート
                    self._set_trump(card.suit)

                print(field)

            winner = self.decide_winner_in_track()
            self.add_point(winner)

            self.field.clear()
            print(field)

            self.track_cnt += 1
            start_player_id = self.get_start_player_id()
            self.set_track(start_player_id = start_player_id)

        self.decide_winner_in_game(field)

class NapoleonGame(Game):
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
