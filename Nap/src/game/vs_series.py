import random

from ..utils import (
    Suit,
    Card,
)

from ..player import (
    Player,
    Takeshi,
)

from .game import (
    SimpleNapGame,
    EasyNapGame,
)

class VSBase:
    """
    VS シリーズの共通の処理
    """
    def _set_player(self):
        """
        """
        raise NotImplementedError()

class VSTakeshi(VSBase):
    """
    たけしと戦う上で共有の処理
    """
    def _set_player(self, how_to_choose: str = "input") -> list[Player]:
        """
        ゲームに参加させるプレイヤーを着席させる

        Args:
            how_to_choose (str): CPU でないプレイヤーがどのようにカードを選択するか
                Player class 参照

        Returns:
            list[Player]: ゲームに参加するプレイヤー
        """
        return [Takeshi(), Player("You", cpu=False, how_to_choose=how_to_choose)]

class SimpleNapVSTakeshi(VSTakeshi, SimpleNapGame):
    """
    たけしとのシンプルなトラックテイキングで勝負 (Takeshi Lv.1)
    
    Attributes:
        describe (str): ゲームの説明
    """
    describe = \
"""
1. シンプルなトリックテイキングゲーム
2. たけしと 1 vs 1 で行う
3. 手札は 3 枚 (3 トリックの勝負)
4. 台札はなし (スートの請求もなし)
5. 切り札は、スペードに固定
6. スートの強さ優先 (spade > heart > diamond > club)
7. 次に数字の強さ優先
8. トリックの先行は、常にたけし
9. ジョーカーなしの 52 枚のカード
"""
    def __init__(self, player_how_to_choose: str = "input"):
        super().__init__(player_how_to_choose = player_how_to_choose,
                         first_message = Takeshi.talk(theme = "introduction"))

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

class EasyNapVSTakeshi(VSTakeshi, EasyNapGame):
    """
    たけしのリベンジ (Takeshi Lv.2)

    Attributes:
        describe (str): ゲームの説明
    """
    describe = \
"""
1. シンプルなトリックテイキングゲーム
2. たけしと 1 vs 1 で行う
3. 手札は 5 枚 (5 トリックの勝負)
4. 台札あり (スートの請求もあり)
5. 切り札は、ランダム
6. 最初のトリックの先行は、ランダム / その後は前のトリックの勝者
7. ジョーカーなしの 52 枚のカード
"""
    def __init__(self, player_how_to_choose: str = "input", first_message: str = None):
        super().__init__(player_how_to_choose = player_how_to_choose,
                         first_message = Takeshi.talk(theme = "introduction"))

    def deal(self) -> None:
        """Deal cards.

        カードを各プレイヤーに配る
        たけしには、クラブのカードを多く渡す
        """
        club_card_num = 3
        takeshi_hand_club = [Card(num = n, suit = Suit.club) for n in range(1, 1 + club_card_num)]

        for player in self.field.players:
            if player.name == "たけし": 
                takeshi_hand = self.field.deck.pull_out(takeshi_hand_club)
                takeshi_hand += self.field.deck.deal(self.hand_num - club_card_num)
                player.take_hand(takeshi_hand)
            else:
                player.take_hand(self.field.deck.deal(self.hand_num))

    def _set_trump(self):
        """
        切り札を設定する

        Note:
            切り札は、クラブ以外でランダム

        """
        self.field.trump = [Suit.spade, Suit.heart, Suit.diamond][random.randint(0, 2)]

class VSTakeshi:
    """
    たけしと戦う上で共有の処理
    """