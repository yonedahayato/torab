from collections.abc import Callable
import random

from pathlib import Path
import sys

BASE_DIR = Path(__file__).parents[3]
sys.path.append(str(BASE_DIR))

from src.player import (
    Player,
)
from src.game import (
    SimpleNapVSTakeshi,
    EasyNapVSTakeshi,
    EasyNapVSShizuka,
    NapVSShizuka,
)

class GUIGameBase:
    """
    ゲームクラスをGPUで実行するためのクラス
    """
    def __init__(self, 
                 delete_button_func: Callable,
                 make_button_func: Callable,
                 message_func: Callable,
                 set_field_func: Callable,
                 set_talk_func: Callable,
                 ):
        """
        Args:
            delete_button_func (Callable): ボタンを削除する関数
            make_button_func (Callable): ボタンを作成する関数
            message_func (Callable): メッセージを行う関数

        Attribures:
            track_cnt (int): トラックを行った回数
            play_cnt (int): あるトラック内で、行われたプレイ数
            is_finish (bool): ゲームが終了しているかどうか
            time_lag (int): Track class の設定
            
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

        self.delete_go_button = delete_button_func
        self.make_go_button = make_button_func
        self.say = set_talk_func
        self.message = message_func
        self.display_field = set_field_func

        self.set_lines()

        # 次に進むボタンを作成
        self.make_go_button(next_action="talk")

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
                self.say(message = message, charactor_name = charactor_name)
            else:
                self.say(message = message)

        else:
            message = self.lines.pop(0)
            if isinstance(message, list):
                message, charactor_name = message
                self.say(message = message, charactor_name=charactor_name)
            else:
                self.say(message = message)

            self.field.message = message
            print(self.field)
            self.display_field(self.field)

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
        self.display_field(self.field)

        self.play_cnt += 1

    def close_track_on_GUI(self) -> None:
        """
        トラックの終了処理
        
        Note:
            次の処理は、next_track
        """
        self.close_track()
        self.display_field(self.field)

        self.make_go_button(next_action = "next_track")

    def next_track_on_GUI(self) -> None:
        """
        新しいトラックの準備
        
        Note:
            次の処理は、play_cpu
        """
        # 次のトラックの準備
        self.next_track()
        self.display_field(self.field)

        self.play_cnt = 0
        self.make_go_button(next_action = "play_cpu")
        
    def close_game_on_GUI(self) -> None:
        """
        ゲームを終了させる

        Note:
            次の処理は restart
        """
        self.close_game()
        self.display_field(self.field)

        self.is_finish = True
        self.make_go_button(next_action = "restart")

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

        self.display_field(self.field, can_play = True)

    def play_cpu(self) -> None:
        """
        プレイヤー以外 (つまり CPU) の操作
        """
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track_on_GUI()
            return

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game_on_GUI()
            return

        next_player = self.track.get_next_player()
        if not next_player.cpu:
            # 次の処理は run (= プレイヤーのプレイ)
            self.play_player(next_player)
            return

        # CPU のプレイ
        self.next_play()
        self.make_go_button(next_action = "play_cpu")
        self.talk(is_in_play = True)
        return

    def go(self, next_action: str):
        """
        メッセージを読んだことがわかった後の処理        

        Args:
            next_action: 次の実行内容
        """
        # ボタンの削除
        self.delete_go_button()

        if len(self.lines) == 1:
            # 最後のおしゃべり
            # 次のアクションは、プレイ
            self.talk()
            self.make_go_button(next_action = "play_cpu")
            return

        elif len(self.lines) > 1:
            # まだまだ、しゃべるぞ
            # 次のアクションは、トーク
            self.talk()
            self.make_go_button(next_action = "talk")
            return

        else:
            # len(lines) == 0
            # 喋ることがなければ何もしない
            pass

        if next_action == "play_cpu":
            self.play_cpu()
        elif next_action == "next_track":
            self.next_track_on_GUI()
        elif next_action == "talk":
            # しゃべることがないのに、トークはできない
            raise Exception(f"next action が異常: {next_action} / 喋れない")
        else:
            raise ValueError(f"next action が異常: {next_action}")

    def run(self, card_id: int) -> None:
        """
        ブラウザからなんらかのイベントが発生し、ゲームを動かす
        (go 以外のブラウザからの入力、カードを選択する、宣言を行うなどを想定)

        Args:
            event (JsProxy): ユーザが発生させたイベント情報
        """
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track_on_GUI()

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game_on_GUI()
            return

        # プレイヤーのプレイ
        next_player = self.track.get_next_player()
        next_player.choose_card_id = card_id

        # self.card_buttons.delete()
        self.next_play()

        # CPU のプレイ
        self.play_cpu()

class VSTakeshiGUIGame(GUIGameBase, SimpleNapVSTakeshi):
    """
    SimpleNapVSTakeshiをGUIで実行するためのクラス
    """
    def __init__(self, 
                 delete_go_button: Callable,
                 make_go_button: Callable,
                 message_func: Callable,
                 set_field_func: Callable,
                 set_talk_func: Callable,
                 ):
        SimpleNapVSTakeshi.__init__(self, player_how_to_choose = "set")
        GUIGameBase.__init__(self, delete_go_button, make_go_button, message_func, 
                             set_field_func, set_talk_func)

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
        
        self.lines = [
            "おまえ、トランプ強いんだってな",
            "ちょっくら、つきあってくれよい!"]
        
        self.lines_in_play = [line for thema, line in takeshi.lines.items() if thema != "introduction"]