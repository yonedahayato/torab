"""
worker.py の GameMaster が利用するゲームを実行するクラス
"""

import random
from pyodide.ffi import JsProxy
from pyscript import document
import sys

sys.path.append("/home/work")
sys.path.append("/pyscript/pyscript/src")

from .button import (
    Buttons,
)

from src.player import Player

from src.game import (
    SimpleNapVSTakeshi,
    EasyNapVSTakeshi,
    EasyNapVSShizuka,
    NapVSShizuka,
)

from src.bid import NapDeclaration

def say(content: str, charactor_name: str = "takeshi") -> None:
    """
    吹き出しを利用して、喋る
    
    Args:
        content (str): しゃべる内容
    """
    fukidasi_area = document.querySelector("#fukidasi")
    fukidasi_area.textContent = content

    charactor_area = document.querySelector("#charactor")

    charactor_area.src = f"./asset/image/charactor/{charactor_name}/v.0.0/main.png"

class BrowserGameBase:
    """
    ゲームクラスをブラウザーで実行するためのクラス
    """
    def __init__(self):
        """
        Attribures:
            track_cnt (int): トラックを行った回数
            play_cnt (int): あるトラック内で、行われたプレイ数
            is_finish (bool): ゲームが終了しているかどうか
            time_lag (int): Track class の設定

            # button
            card_buttons (CardButtons): カードボタンを表示を管理
            go_buttons (CardButtons): Go ボタンを表示を管理
            
        Note:
            処理の流れ
                1. 必要な設定を行う
                2. ボタンを作成に必要なクラスをインスタンス化
                3. 整理を設置

            次の処理は、talk
        """
        self.track_cnt = 0
        self.play_cnt = 0
        self.is_finish = False
        self.time_lag = 0.1

        self.card_buttons = Buttons()
        self.go_buttons = Buttons()

        self.set_lines()
        self.make_go_buttons(next_action = "talk")

    def set_lines(self) -> None:
        """
        セリフを設定する
        """
        raise ImportError("set_lines を実装してください")

    def talk(self, is_in_play: bool = False):
        """
        喋るメッセージを表示させる処理
        
        Args:
            is_in_play (bool): プレイ中かどうか
        """
        if is_in_play:
            message = random.choice(self.lines_in_play)
            if isinstance(message, list):
                message, charactor_name = message
                say(content = message, charactor_name=charactor_name)
            else:
                say(content = message)

        else:
            message = self.lines.pop(0)
            if isinstance(message, list):
                message, charactor_name = message
                say(content = message, charactor_name=charactor_name)
            else:
                say(content = message)

            self.field.message = message
            print(self.field)

    def make_go_buttons(self, next_action: str) -> None:
        """
        go button を作成する
        
        Args:
            next_action (str): Go button には、次のアクションの情報を追記する
        """
        self.go_buttons.make(text = "Next", func_name = "game.go", value = next_action)

    def next_play(self) -> None:
        """
        プレイを行う
        
        Note:
            CPU / プレイヤー どちらかのプレイ
            Track.__next__ が動いているだけなので、この関数内では判断できない
            Game class でいうところの play method
        """
        self.field = next(self.track)
        print(self.field)
        self.play_cnt += 1

    def close_track_on_browser(self) -> None:
        """
        トラックの終了処理
        
        Note:
            次の処理は、next_track
        """
        self.close_track()
        self.make_go_buttons(next_action = "next_track")

    def next_track_on_browser(self) -> None:
        """
        新しいトラックの準備
        
        Note:
            次の処理は、play_cpu
        """
        # 次のトラックの準備
        self.next_track()

        self.play_cnt = 0
        self.make_go_buttons(next_action = "play_cpu")
        
    def close_game_on_browser(self) -> None:
        """
        ゲームを終了させる
        """
        self.close_game()        
        self.is_finish = True

    def play_player(self, player: Player) -> None:
        """
        プレイヤーへ操作を行わせるための前処理
        
        Args:
            player (Player): プレイヤーのクラス

        Note:
            カードの表示の処理にクリックできるカードとできないカードを
            指定するための処理はここで行う
        """
        # 出せるカードの情報をターミナル上で表示
        _ = player.check_cards_can_submit()

        self.card_buttons.make_card(cards = player.cards)

    def play_cpu(self) -> None:
        """
        プレイヤー以外 (つまり CPU) の操作
        """
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track_on_browser()
            return

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game_on_browser()
            return

        next_player = self.track.get_next_player()
        if not next_player.cpu:
            # 次の処理は run (= プレイヤーのプレイ)
            self.play_player(next_player)
            return

        # CPU のプレイ
        self.next_play()
        self.make_go_buttons(next_action = "play_cpu")
        self.talk(is_in_play = True)
        return

    # button による操作
    def go(self, event: JsProxy) -> None:
        """
        メッセージを読んだことがわかった後の処理
        
        Args:
            event (JsProxy): メッセージの確認後のイベントのため、情報としては何もない
        """
        self.go_buttons.delete()

        next_action = event.target.getAttribute('value')
        
        if len(self.lines) == 1:
            # 最後のおしゃべり
            # 次のアクションは、プレイ
            self.talk()
            self.make_go_buttons(next_action = "play_cpu")
            return

        elif len(self.lines) > 1:
            # まだまだ、しゃべるぞ
            # 次のアクションは、トーク
            self.talk()
            self.make_go_buttons(next_action = "talk")
            return

        else:
            # len(lines) == 0
            # 喋ることがなければ何もしない
            pass

        if next_action == "play_cpu":
            self.play_cpu()
        elif next_action == "next_track":
            self.next_track_on_browser()
        elif next_action == "talk":
            # しゃべることがないのに、トークはできない
            raise Exception(f"next action が異常: {next_action} / 喋れない")
        else:
            raise ValueError(f"next action が異常: {next_action}")

    # button による操作
    def run(self, event: JsProxy) -> None:
        """
        ブラウザからなんらかのイベントが発生し、ゲームを動かす
        (go 以外のブラウザからの入力、カードを選択する、宣言を行うなどを想定)

        Args:
            event (JsProxy): ユーザが発生させたイベント情報
        """
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track_on_browser()

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game_on_browser()
            return

        # プレイヤーのプレイ
        next_player = self.track.get_next_player()
        card_id = int(event.target.getAttribute('value'))
        next_player.choose_card_id = card_id
        self.card_buttons.delete()
        self.next_play()

        # CPU のプレイ
        self.play_cpu()

class BrowserGameWithBid(BrowserGameBase):
    """
    ゲームクラスをブラウザーで実行するためのクラス
    bidを行うゲームを扱う

    Attributes:
        declaration_buttons (Buttons): 宣言を選択するボタン
        is_bid_close (bool): bid を一度でも完了したかどうか
    """
    def __init__(self):
        super().__init__()
        self.declaration_buttons = Buttons()
        self.is_bid_close = False

    def next_bid(self) -> None:
        """
        bidを行う
        
        Note:
            CPU / プレイヤー どちらかのbid
            Bid.__next__ が動いているだけなので、この関数内では判断できない
        """
        self.field = next(self.bid_manager)
        print(self.field)
        self.bid_cnt += 1

    def close_bid_on_browser(self):
        """
        bidの終了処理
        
        Note:
            次の処理は、next_track
        """
        self.close_bid()

        self.make_go_buttons(next_action = "play_cpu")
        self.is_bid_close = True

    def start_bid(self) -> None:
        """
        bidの準備
        
        Note:
            次の処理は、bid_cpu
        """
        self.bid_cnt = 0

        self.field.message = "Bidを行います"
        print(self.field)

        self.make_go_buttons(next_action = "bid_cpu")

    def bid_player(self, player: Player) -> None:
        """
        プレイヤーへbidを行わせるための前処理
        
        Args:
            player (Player): プレイヤーのクラス
        """

        # 選択できるbidの情報をターミナル上で表示
        # 選択できる宣言は、最も強い宣言よりも強い宣言
        declarable_list = self.bid_manager.best_declaration.get_declarable_list()
        print(declarable_list)

        self.declaration_buttons.make_declarations(declarable_list)

    def bid_cpu(self) -> None:
        """
        プレイヤー以外 (つまり CPU) のbid
        """
        if self.bid_manager.is_finish():
            # ビッドが終了している場合
            self.close_bid_on_browser()
            return

        next_bid_player = self.bid_manager.get_next_player()
        if not next_bid_player.cpu:
            # 次の処理は run (= プレイヤーのビッド)
            self.bid_player(next_bid_player)
            return

        # CPU のプレイ
        self.next_bid()
        self.make_go_buttons(next_action = "bid_cpu")
        self.talk(is_in_play = True)
        return

    def next_play(self) -> None:
        """
        プレイを行う
        
        Note:
            CPU / プレイヤー どちらかのプレイ
            Track.__next__ が動いているだけなので、この関数内では判断できない
            Game class でいうところの play method
        """
        self.field = next(self.track)

        if self.track_cnt == 0 and self.play_cnt == 0:
            card = self.field.cards[str(self.bid_manager.declarer)]
            #切り札は、最初のトラックのリードのスート
            self._set_trump(card.suit)

        print(self.field)

        self.play_cnt += 1

    def close_game_on_browser(self) -> None:
        """
        ゲームを終了させる
        """
        self.decide_winner_in_game()        
        self.is_finish = True

    # button による操作
    def go(self, event: JsProxy) -> None:
        """
        メッセージを読んだことがわかった後の処理
        
        Args:
            event (JsProxy): メッセージの確認後のイベントのため、情報としては何もない
        """
        self.go_buttons.delete()

        next_action = event.target.getAttribute('value')
        
        if len(self.lines) == 1:
            # 最後のおしゃべり
            # 次のアクションは、ビッドに開始
            self.talk()
            self.make_go_buttons(next_action = "start_bid")
            return

        elif len(self.lines) > 1:
            # まだまだ、しゃべるぞ
            # 次のアクションは、トーク
            self.talk()
            self.make_go_buttons(next_action = "talk")
            return

        else:
            # len(lines) == 0
            # 喋ることがなければ何もしない
            pass

        if next_action == "start_bid":
            self.start_bid()
        elif next_action == "bid_cpu":
            self.bid_cpu()
        elif next_action == "play_cpu":
            self.play_cpu()
        elif next_action == "next_track":
            self.next_track_on_browser()
        elif next_action == "talk":
            # しゃべることがないのに、トークはできない
            raise Exception(f"next action が異常: {next_action} / 喋れない")
        else:
            raise ValueError(f"next action が異常: {next_action}")

    # button による操作
    def run(self, event: JsProxy) -> None:
        """
        ブラウザからなんらかのイベントが発生し、ゲームを動かす
        
        Args:
            event (JsProxy): ユーザが発生させたイベント情報
        """
        if self.is_bid_close:
            # bid は、すでに行われた
            pass

        elif self.bid_manager.is_finish():
            # ビッドが終了したので、ゲームを開始する準備を行う
            self.declaration_buttons.delete()
            self.close_bid_on_browser()
            return

        else:
            # プレイヤーのプレイ
            next_player = self.bid_manager.get_next_player()
            declare_id = int(event.target.getAttribute('value'))
            next_player.choose_declare_id = declare_id
            self.declaration_buttons.delete()
            self.next_bid()

            # CPU のプレイ
            self.bid_cpu()
            return

        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track_on_browser()

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game_on_browser()
            return

        # プレイヤーのプレイ
        next_player = self.track.get_next_player()
        card_id = int(event.target.getAttribute('value'))
        next_player.choose_card_id = card_id
        self.card_buttons.delete()
        self.next_play()

        # CPU のプレイ
        self.play_cpu()

class VSTakeshiBrowserGame(BrowserGameBase, SimpleNapVSTakeshi):
    """
    SimpleNapVSTakeshiをブラウザーで実行するためのクラス
    """
    def __init__(self):
        SimpleNapVSTakeshi.__init__(self, player_how_to_choose = "set")
        BrowserGameBase.__init__(self)

    def set_lines(self) -> None:
        """
        セリフを設定する
        
        Attributes:
            lines (list[str]): セリフ集
            
        Note:
            最初に表示させておきたいセリフを取得し、表示させる
            その後喋る内容も設置する
        """
        takeshi = self.field.get_player(name = "たけし")
        
        say(takeshi.lines["introduction"])
        self.lines = [
            "おまえ、トランプ強いんだってな",
            "ちょっくら、つきあってくれよい!"]
        
        self.lines_in_play = [line for thema, line in takeshi.lines.items() if thema != "introduction"]

class VSTakeshiLv2BrowerGame(VSTakeshiBrowserGame, EasyNapVSTakeshi):
    """
    """
    describe = EasyNapVSTakeshi.describe
    def __init__(self):
        super().__init__()

    def play_player(self, player: Player) -> None:
        """
        プレイヤーへ操作を行わせるための前処理
        
        Args:
            player (Player): プレイヤーのクラス
            
        Note:
            台札によるスートの請求があるゲームがある
            出せないカードは、クリックできないようにする
        """
        cards_can_submit = player.check_cards_can_submit(lead_suit = self.field.lead)
        cards_can_submit = [str(c) for c in cards_can_submit]
        disable = [str(hand) not in cards_can_submit for hand in player.cards]
        self.card_buttons.make_card(cards = player.cards, disable = disable)

    def deal(self) -> None:
        """
        EasyNapVSTakesiのゲーム内容に準じたカードの配り方があるため、それを実行
        """
        EasyNapVSTakeshi.deal(self)

class VSShizukaBrowserGame(BrowserGameBase, EasyNapVSShizuka):
    """
    SimpleNapVSTakeshiをブラウザーで実行するためのクラス
    """
    def __init__(self):
        self.first_message = "私も混ぜてもらえる？"
        EasyNapVSShizuka.__init__(self, player_how_to_choose = "set", first_message = self.first_message)
        BrowserGameBase.__init__(self)

    def set_lines(self) -> None:
        """
        セリフを設定する
        
        Attributes:
            lines (list[str]): セリフ集
            
        Note:
            最初に表示させておきたいセリフを取得し、表示させる
            その後喋る内容も設置する
        """
        takeshi = self.field.get_player(name = "たけし")
        shizuka = self.field.get_player(name = "しずか")
        
        say(self.first_message, charactor_name="shizuka")
        self.lines = [
            ["あなた達、トランプできるの？", "shizuka"],
            ["こいつなんだ!?生意気だな", "takeshi"],
            ]
        
        self.lines_in_play = [[line, "takeshi"] for thema, line in takeshi.lines.items() if thema != "introduction"]
        self.lines_in_play += [[line, "shizuka"] for thema, line in shizuka.lines.items() if thema != "introduction"]

    def play_player(self, player: Player) -> None:
        """
        プレイヤーへ操作を行わせるための前処理
        
        Args:
            player (Player): プレイヤーのクラス
            
        Note:
            台札によるスートの請求があるゲームがある
            出せないカードは、クリックできないようにする
        """
        cards_can_submit = player.check_cards_can_submit(lead_suit = self.field.lead)
        cards_can_submit = [str(c) for c in cards_can_submit]
        disable = [str(hand) not in cards_can_submit for hand in player.cards]
        self.card_buttons.make_card(cards = player.cards, disable = disable)

class VSShizukaLv2BrowserGame(BrowserGameWithBid, NapVSShizuka):
    """
    NapVSShizukaをブラウザーで実行するためのクラス

    Note:
        VSShizukaBrowserGame は、play_playerを利用するためのみの目的で、継承
    """
    def __init__(self):
        self.first_message = "面白くなってきたわね、ギアを上げるわ"
        NapVSShizuka.__init__(self, player_how_to_choose = "set", first_message = self.first_message)
        BrowserGameWithBid.__init__(self)

    def set_lines(self) -> None:
        """
        セリフを設定する
        
        Attributes:
            lines (list[str]): セリフ集
            
        Note:
            最初に表示させておきたいセリフを取得し、表示させる
            その後喋る内容も設置する
        """
        takeshi = self.field.get_player(name = "たけし")
        shizuka = self.field.get_player(name = "しずか")
        
        say(self.first_message, charactor_name="shizuka")
        self.lines = [
            ["Napは理解しているわね？", "shizuka"],
            ["当たり前だろ!?生意気だな", "takeshi"],
            ]
        
        self.lines_in_play = [[line, "takeshi"] for thema, line in takeshi.lines.items() if thema != "introduction"]
        self.lines_in_play += [[line, "shizuka"] for thema, line in shizuka.lines.items() if thema != "introduction"]

    def play_player(self, player: Player) -> None:
        """
        プレイヤーへ操作を行わせるための前処理
        
        Args:
            player (Player): プレイヤーのクラス
            
        Note:
            台札によるスートの請求があるゲームがある
            出せないカードは、クリックできないようにする

        Todo:
            この処理の共通化
        """
        cards_can_submit = player.check_cards_can_submit(lead_suit = self.field.lead)
        cards_can_submit = [str(c) for c in cards_can_submit]
        disable = [str(hand) not in cards_can_submit for hand in player.cards]
        self.card_buttons.make_card(cards = player.cards, disable = disable)