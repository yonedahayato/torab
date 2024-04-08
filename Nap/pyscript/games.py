"""
worker.py の GameMaster が利用するゲームを実行するクラス
"""

import random
from pyodide.ffi import JsProxy
from pyscript import document
import sys

sys.path.append("/home/work")
sys.path.append("/pyscript/pyscript")

from button import (
    Buttons,
)

from src.game import (
    SimpleNapVSTakeshi,
)

def say(content: str) -> None:
    """
    吹き出しを利用して、喋る
    
    Args:
        content (str): しゃべる内容
    """
    fukidasi_area = document.querySelector("#fukidasi")
    fukidasi_area.textContent = content

class VSTakeshiBrowserGame(SimpleNapVSTakeshi):
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
        super().__init__(player_how_to_choose = "set")
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

    def talk(self, is_in_play: bool = False):
        """
        喋るメッセージを表示させる処理
        
        Args:
            is_in_play (bool): プレイ中かどうか
        """
        if is_in_play:
            message = random.choice(self.lines_in_play)
        else:
            message = self.lines.pop(0)
            self.field.message = message
            print(self.field)

        say(content = message)

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
        """
        self.field = next(self.track)
        print(self.field)
        self.play_cnt += 1

    def close_track(self):
        """
        トラックの終了処理
        
        Note:
            次の処理は、next_track
        """
        winner = self.decide_winner_in_track()
        self.add_point(winner)

        self.field.message = f"Track {self.track_cnt} を {winner} がとりました"
        print(self.field)

        self.make_go_buttons(next_action = "next_track")

    def next_track(self) -> None:
        """
        新しいトラックの準備
        
        Note:
            次の処理は、play_cpu
        """
        self.field.clear()
        self.set_track(start_player_id = 0)

        self.play_cnt = 0
        self.track_cnt += 1

        self.field.message = "次の Track です"
        print(self.field)

        self.make_go_buttons(next_action = "play_cpu")
        
    def close_game(self) -> None:
        """
        ゲームを終了させる
        """
        winner = self.decide_winner_in_game()
        self.field.message = f"このゲームの勝者は、{winner} です"
        print(self.field)
        
        self.is_finish = True

    def play_cpu(self) -> None:
        """
        プレイヤー以外 (つまり CPU) の操作
        """
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track()
            return

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game()
            return

        next_player = self.track.get_next_player()
        if not next_player.cpu:
            # 次の処理は。run (= プレイヤーのプレイ)
            print("出すカードを入力してください")
            print([f"{i}: {c}" for i, c in enumerate(next_player.cards)])
            # self.card_buttons.make(card_num = len(next_player.cards))
            self.card_buttons.make_card(cards = next_player.cards)
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
            self.next_track()
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
        if self.play_cnt == len(self.field.players):
            # 全てのプレイヤーが、プレイし終わっていたら、
            # その tack が終了しているとして、新しいトラックを作成する
            self.close_track()

        if self.track_cnt == self.hand_num:
            # すべてのトラックが終了したら、ゲームを終了させる手続きに入る
            self.close_game()
            return

        # プレイヤーのプレイ
        next_player = self.track.get_next_player()
        card_id = int(event.target.getAttribute('value'))
        next_player.choose_card_id = card_id
        self.card_buttons.delete()
        self.next_play()

        # CPU のプレイ
        self.play_cpu()