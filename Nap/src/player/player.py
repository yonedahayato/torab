import random
from typing import Literal

from ..utils import (
    Suit,
    Card,
    Logger,
)

from .declear import Declear

logger = Logger()
print = logger.log_print

class Player:
    """Player class.
    プレイヤークラス

    Attributes:
        is_nap (bool): ナポレオンかどうか
        is_adjutant (bool): 副官かどうか
        is_allied (bool): 連合軍かどうか

        point (int): プレイヤーが所持してる点数
        cards (list[Card]): プレイヤーのハンド

    Note:
        プレイヤーは、ナポレオン、副官、連合軍のいずれかである

        プレイヤーが行うことができることは、以下の通り
            1. 手札を受け取る
            2. 宣言する
            3. カードを出す
        
        CPU は、ランダムに宣言する
    """

    def __init__(self, 
                 name: str = "Unknown", 
                 cpu: bool = False, 
                 how_to_choose: str = "input"):
        """Constructor.
        
        Attributes:
            name (str): プレイヤーの名前
            cpu (bool): CPU かどうか
            how_to_choose (str): プレイヤークラスの choose_card メソッドの挙動の方法
                input: input method を利用
                set: 変数を格納することでカードを選択する
        """
        self.name = name
        self.cpu = cpu
        if how_to_choose not in ["input", "set"]:
            raise ValueError(f"プレイヤーのカードの選択方法が異常: {how_to_choose}")
        self.how_to_choose = how_to_choose

        self.is_nap = False
        self.is_adjutant = False
        self.is_allied = False

        self.point = 0
        self.cards = []
        self._choose_card_id = None
        self._choose_declare_id = None

    def __repr__(self):
        return f"Player(name={self.name})"

    def __str__(self) -> str:
        """String.
        
        Returns:
            str: プレイヤーの名前
        """
        return self.name

    @property
    def choose_card_id(self) -> int:
        """
        
        choose_card_id の getter

        Attributes:
            choose_card_id (int): 選択するカードをあらかじめ格納するために利用する
            
        Returns:
            int: choose_card_id の値
        """
        return self._choose_card_id
    
    @choose_card_id.setter
    def choose_card_id(self,
                       card_id: int,
                    ) -> None:
        """
        
        choose_card_id の setter
        
        Args:
            card_id (int): 選択するカード
        """
        self._choose_card_id = card_id

    def take_hand(self, 
                  cards: list[Card]
                ) -> None:
        """
        カードを受け取る

        Args:
            cards (list): List of cards.
        """
        self.cards = sorted(cards)
        
    def show_hand(self, 
                  hint: str = "no", 
                  is_force: bool = False
                ) -> list[Card]:
        """Show hand.
        手札を開示する
        
        Args:
            hint (str): CPU が開示する際に、ヒントを持たせるかどの程度ヒントを持たせるか
                no : ヒントなし
                mark-{n} : マークの開示
                num-{n} : 数字の開示
            is_force (bool): 強制的にカードを開示させる

        Return
            list[Card]: 開示する情報
            
        Note:
            (基本的に) CPU は、カードの種類までは開示しない
        """
        if hint not in ["no", "mark-1", "num-1"]:
            raise ValueError(f"想定していないヒントの値: {hint}")

        if is_force:
            hand = self.cards

        elif self.cpu and hint == "mark-1":
            hand = []
            for cnt, card in enumerate(self.cards):
                if cnt < 1:
                    hand.append(f"{card.suit.mark}-?")
                else:
                    hand.append("?")

        elif self.cpu and hint == "num-1":
            hand = []
            for cnt, card in enumerate(self.cards):
                if cnt < 1:
                    hand.append(f"?-{card.get_num_str()}")
                else:
                    hand.append("?")

        elif self.cpu:
            hand = ["?" for _ in self.cards]

        else:
            hand = self.cards

        return hand
    
    def check_cards_can_submit(self, 
                               lead_suit: Suit = None
                            ) -> list[Card]:
        """
        CPU でないプレイヤーが、カードを確認する
        
        Args:
            lead_suit (Suit): 台札のスート
            
        Returns:
            list[Card]: 出せるカード
        """
        if lead_suit is None:
            # リードがなければ、何も表示しない
            cards_can_submit = self.cards
        elif lead_suit not in [c.suit for c in self.cards]:
            print("どのカードでも出せます。")
            cards_can_submit = self.cards
        else:
            cards_can_submit = [c for c in self.cards if c.suit == lead_suit]
            cards_can_submit_text = [f"{i}: {c}" for i, c in enumerate(self.cards) if c.suit == lead_suit]
            print(f"出せるカードは、{cards_can_submit_text} です")

        print("カードを選んでください。")
        print([f"{i}: {c}" for i, c in enumerate(self.cards)])

        return cards_can_submit

    def input_card(self, lead_suit: Suit):
        """
        標準入力を利用して、カードを選択する

        Args:
            lead_suit (Suit): 要求されているスート
        """
        cards_can_submit = self.check_cards_can_submit(lead_suit = lead_suit)

        try:
            card_id = int(input("出すカードの番号: "))
        except ValueError:
            print("\nカードの番号を入力してください。")
            card_id = self.input_card(lead_suit = lead_suit)
            
        if len(self.cards) <= card_id:
            print("\n入力の範囲を超えています。")
            card_id = self.input_card(lead_suit = lead_suit)
            
        if str(self.cards[card_id]) not in [str(c) for c in cards_can_submit]:
            print("\nそのカードは出せません。")
            card_id = self.input_card(lead_suit = lead_suit)

        return card_id
    
    def input_declare(self, declarable_list: list) -> int:
        """
        標準入力を利用して、宣言を行う

        Args:
            declarable_list (list): 宣言可能な宣言の一覧

        Returns:
            int: 選択された宣言のid
        """
        print("宣言を選んでください")
        for d_id, declare in enumerate(declarable_list):
            print(f"{d_id}: {declare}")

        try:
            declare_id = int(input("宣言の番号: "))
        except ValueError:
            print("\n宣言の番号を入力してください。")
            declare_id = self.input_declare(declarable_list)

        return declare_id

    def choose_card(self, lead_suit: Suit) -> Card:
        """
        CPU でないプレイヤーが、カードを選ぶ処理
        
        Args:
            lead_suit (Suit): 台札のスート

        Returns:
            Card: 選択したカード
            
        Note:
            input を使うケース
            set (変数) を使うケース
                利用後は、削除 (Noneを代入)
        """

        if self.how_to_choose == "input":
            card_id = self.input_card(lead_suit = lead_suit)
            
        elif self.how_to_choose == "set":
            card_id = self.choose_card_id
            self.choose_card_id = None

        card = self.cards.pop(card_id)

        return card

    def choose_declare(self, declarable_list: list) -> any:
        """
        CPU でないプレイヤーが、宣言を行う処理

        Args:
            declarable_list (list): 宣言可能な宣言の一覧

        Returns:
            Declare: 選択された宣言
            
        Note:
            input を使うケース
            set (変数) を使うケース
                利用後は、削除 (Noneを代入)
        """
        if self.how_to_choose == "input":
            declare_id = self.input_declare(declarable_list=declarable_list)
            
        elif self.how_to_choose == "set":
            declare_id = self.choose_declare_id
            self.choose_declare_id = None

        declare = declarable_list[declare_id]

        return declare

    def play_card(self, 
                  is_random: bool = False, 
                  lead_suit: Suit = None) -> Card:
        """Play card.
        カードを出す
        
        Args:
            field (Field): フィールド
            is_random (bool): ランダムにカードを出すかどうか
            
        Returns:
            Card: カード
            
        Note:
            ランダム or CPU ならば、ランダムにカードを選択する
                lead_suit がない、もしくは手札に lead_suit がなければ、ランダムに選択する
        """

        if is_random or self.cpu:
            
            if lead_suit is None or lead_suit not in [c.suit for c in self.cards]:
                cards = self.cards
            else:
                cards = [c for c in self.cards if c.suit == lead_suit]

            card_id = random.randrange(len(cards))
            card = self.cards.pop(card_id)

        else:
            card = self.choose_card(lead_suit)

        return card

    def declare(self, 
                declarable_list: list,
                is_random: bool = False,
            ) -> any:
        """Declare.
        宣言する
        
        Args:
            declarable_list (list): 宣言可能な一覧
            is_random (bool): ランダムに宣言するかどうか

        Returns:
            Declear: 宣言

        Note:
            ランダム or CPU ならば、ランダムに宣言を行う
        """

        if is_random or self.cpu:
            declear = random.choice(declarable_list)

        else:
            declear = self.choose_declare(declarable_list)

        return declear