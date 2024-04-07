"""
pyscript における worker に動いてもらう処理
main() を直接実行しているため、他の python file から参照は非推奨
"""

from pyscript import document
from pyodide.ffi import JsProxy

import sys

sys.path.append("/home/work")
sys.path.append("/pyscript/pyscript")

from games import VSTakeshiBrowserGame
from button import (
    make_button,
)

class GameMaster:
    """
    ゲームマスター
    
    Attributes:
        games (dict[str: GameClass]): ゲームの情報

    Note:
        ゲームの選択などを行う
    """
    games = {
        "VS Takeshi LV.1": VSTakeshiBrowserGame
    }

    def __init__(self):
        self.start()

    def start(self):
        """
        ゲームの選択する画面を作成する
        """
        print("ゲームを選択してください")
        self.select_area = document.querySelector("#select")
        self.buttons = []
        for game_name in self.games.keys():
            button = make_button(value = game_name, func_name="game.select")
            self.select_area.appendChild(button)
            self.buttons.append(button)
            
    def describe(self, text: str):
        """
        ゲームの説明をする
        
        Args:
            text(str): ゲームの説明
            
        Attributes:
            describe_area (JsProxy): 説明を挿入するエリア
        """
        self.describe_area = document.querySelector("#describe")
        self.p_list = []
        for text_line in text.split("\n"):
            if text_line == "":
                continue
            p = document.createElement('p')
            p.textContent = text_line
            self.describe_area.appendChild(p)
            self.p_list.append(p)

    def select(self, event) -> None:
        """
        ゲームの選択
        
        Note:
            選択後、ボタンを削除
            選択後、ゲームの説明を表示する
        """
        game_name = event.target.getAttribute('value')
        game_class = self.games.get(game_name, None)
        if game_class is None:
            raise Exception("ゲームの選択に失敗")

        # ゲーム決定
        self.game = game_class()
        
        # ゲームの説明を表示
        self.describe(game_class.describe)

        # button を削除
        for b in self.buttons:
            self.select_area.removeChild(b)            
        self.select_area = []

    def go(self, event: JsProxy) -> None:
        """
        メッセージを読んだことがわかった後の処理
        
        Args:
            event (JsProxy): メッセージの確認後のイベントのため、情報としては何もない
        """
        self.game.go(event)
        if self.game.is_finish:
            self.start()

    def run(self, event: JsProxy) -> None:
        """
        ゲームを実行する
        """
        self.game.run(event)
        if self.game.is_finish:
            self.start()

game = GameMaster()