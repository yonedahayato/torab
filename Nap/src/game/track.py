import time

from ..utils import (
    Card,
    Suit,
)

from ..field import (
    Field,
)

from ..player import (
    Player,
)

class Track:
    """1 回のゲームを管理するクラス
    
    Attributes:
        play_cnt (int): そのトラックの中で何回プレイが行われたか
        lead_suit (int): 台札のスート

    Note:
        このクラスでは、以下のことを行う
        1. トラックの処理の実行
        2. そのトラックにおける勝者の決定
    """
    def __init__(self, field: Field, start_player_id: int, time_lag: int = 0):
        """Constructor.
        Attributes:
            field (Field): フィールド
            start_player_id (int): 最初にプレイをするプレイヤーの番号
            time_lag (int): トラック内のひとつのプレイの間に時間を停止させる時間 [s]
        """
        self.field = field
        self.start_player_id = start_player_id
        self.time_lag = time_lag

        self.play_cnt = 0
        self.lead_suit = None

    def __iter__(self):
        return self

    def __next__(self):
        """
        トラックの中の一人分のプレイの処理
        
        Note:
            処理の流れ
                1. プレイを行うプレイヤーを決定
                2. カードを提出、切り札の決定
                3. play_cnt をインクルーメントする
        """
        if self.play_cnt >= len(self.field.players):
            raise StopIteration

        player_id = (self.start_player_id + self.play_cnt) % len(self.field.players)
        player = self.field.players[player_id]

        card = self.play(player)

        self.field.put_card(player.name, card)
        self.field.message = f"{player.name} が {card} を出した"

        # closing
        self.play_cnt += 1
        time.sleep(self.time_lag)
        return self.field
    
    def play(self, player: Player) -> Card:
        """
        決められたプレイ処理を実行する
        
        Args:
            player (Player): プレイを実行するプレイヤー
            
        Returns:
            Card: プレイをした結果、提出するカード
            
        Note:
            初めに出したカードのスートを台札とする
        """
        card = player.play_card()
        if self.play_cnt == 0:
            self.lead_suit = card.suit
            
        return card
    
    def get_next_player(self) -> Player:
        """
        次にプレイするプレイヤーの情報を取得する
        """
        player_id = (self.start_player_id + self.play_cnt) % len(self.field.players)
        return self.field.players[player_id]


class SimpleTrack(Track):
    """
    シンプルなルールのトラック

    Attributes:
        field (Field): フィールド
        start_player_id (int): 最初にプレイをするプレイヤーの番号
        time_lag (int): トラック内のひとつのプレイの間に時間を停止させる時間 [s]

    Note:
        切り札のスートは固定する
    """
    def __init__(self, field: Field, start_player_id: int, time_lag: int = 0):
        super().__init__(field, start_player_id, time_lag)

    def play(self, player: Player) -> Card:
        """
        決められたプレイ処理を実行する
        
        Args:
            player (Player): プレイを実行するプレイヤー
            
        Note:
            初めに出したスートが、切り札にしない
        """
        card = player.play_card()
        return card

class NapTrack(Track):
    """
    ナポレオンにおけるトラック
    
    ToDo:
        勝敗の判定は、Game class で行う
    """
    def play(self, 
             display: bool = False, 
             is_first: bool = False):
        """Play a trak.
        
        Args:
            display (bool): 出したカードを表示するかどうか
            is_first (bool): 最初のプレイ(トラック)かどうか
                最初のプレイ(トラック)かどうかで、カードの強弱が変わる可能性がある

        Note:
            トラックの流れは以下の通り
                1. 各プレイヤーがカードを出す
                    最初に出したカードが、切り札となる
                2. 出されたカードの強さを比較する

            最初のトラックは、特殊なカードの効果が発動しない
        """
        for cnt, player in enumerate(self.field.players):
            card = player.play_card()
            if cnt == 0:
                self.field.trump = card.suit

            self.field.put_card(player.name, card)
            self.field.message = f"{player.name} が {card} を出した"

            if display:
                print(self.field)

        print(f"\n場に出たカードは {[name + ' : ' + str(c) for name, c in self.field.cards.items()]} です")
        print(self.field)
        
        winner = self.winner()
        return winner
        
    def winner(self) -> Player:
        """Decide a winner.
        勝者を決める
        
        Returns:
            Player: 勝者
            
        Note:
            各プレイヤーがフィールドに出したカードの強さを比較して、勝者を決める
        """
        winner_card = max(list(self.field.cards.values()), 
                          key = lambda x: (self.field.suit_strength(x.suit), x.num))
        
        def get_key(dictionary, value):
            """value から key を取得する
            """
            for k, v in dictionary.items():
                if str(v) == str(value):
                    return k
            return None

        winner = get_key(self.field.cards, winner_card)
        return winner