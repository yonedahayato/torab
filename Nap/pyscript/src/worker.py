"""
pyscript における worker に動いてもらう処理
main() を直接実行しているため、他の python file から参照は非推奨
"""

from pyscript import document
from pyodide.ffi import JsProxy

import sys

sys.path.append("/home/work")
sys.path.append("/pyscript/pyscript/src")

from utils.games import (
    VSTakeshiBrowserGame,
    VSTakeshiLv2BrowerGame,
    VSShizukaBrowserGame,
    VSShizukaLv2BrowserGame,
)
from utils.button import make_button

class GameMaster:
    """
    ゲームマスター
    
    Attributes:
        games (dict[str: GameClass]): ゲームの情報

    Note:
        ゲームの選択などを行う
    """
    games = {
        "VS Takeshi Lv.1": VSTakeshiBrowserGame,
        "VS Takeshi Lv.2": VSTakeshiLv2BrowerGame,
        "VS Shizuka Lv.1": VSShizukaBrowserGame,
        "VS Shizuka Lv.2": VSShizukaLv2BrowserGame,
    }

    def __init__(self):
        """
        
        Attributes:
            titile_area (JsProxy): タイトルの情報
            feild_area (JsProxy): フィールドの情報
        """
        self.title_area = document.querySelector("#title")
        self.feild_area = document.querySelector("#feild")

        self.start()

    def start(self) -> None:
        """
        ゲームの選択する画面を作成する
        
        Note:
            選択するボタンを作成する
        """
        print("ゲームを選択してください")
        self.select_area = document.querySelector("#select")
        self.buttons = []
        for game_name in self.games.keys():
            button = make_button(value = game_name, func_name="game.select")
            self.select_area.appendChild(button)
            self.buttons.append(button)

    def restart(self) -> None:
        """
        ゲームを選択する画面を整え、再度ゲームを選択させる
        """
        self.title_area.textContent = "Nap CLI"
        self.start()
        self.describe_area.removeChild(self.ul_tag)

    def describe(self, game_name: str, text: str):
        """
        ゲームの説明をする
        
        Args:
            game_name: ゲーム名
            text(str): ゲームの説明
            
        Attributes:
            describe_area (JsProxy): 説明を挿入するエリア
            
        Note:
            処理の流れ
                タイトルを変更
                ルールの説明を表示
        """
        self.title_area.textContent = game_name

        self.describe_area = document.querySelector("#describe")

        self.ul_tag = document.createElement('ul')
        self.ul_tag.setAttribute("class", "note")

        self.li_list = []
        for text_line in text.split("\n"):
            if text_line == "":
                continue
            li = document.createElement('li')
            li.textContent = text_line
            self.ul_tag.appendChild(li)
            self.li_list.append(li)
        self.describe_area.appendChild(self.ul_tag)

    def select(self, event) -> None:
        """
        ゲームの選択
        
        Note:
            選択後、ボタンを削除
            選択後、ゲームの説明を表示する
        """
        # ゲーム名の取得
        game_name = event.target.getAttribute('value')

        # ゲームクラスの取得
        game_class = self.games.get(game_name, None)
        if game_class is None:
            raise Exception("ゲームの選択に失敗")

        # ゲーム決定
        self.game = game_class()
        self.feild_area.textContent = str(self.game.field)

        # ゲームのタイトルと説明を表示
        self.describe(game_name, game_class.describe)

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
        self.feild_area.textContent = str(self.game.field)

        if self.game.is_finish:
            self.restart()

    def run(self, event: JsProxy) -> None:
        """
        ゲームを実行する
        
        Args:
           event (JsProxy): ゲームを動かすための情報を含んでいる 
        """
        self.game.run(event)
        self.feild_area.textContent = str(self.game.field)

        if self.game.is_finish:
            self.restart()

game = GameMaster()