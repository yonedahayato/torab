"""
html 上にボタンを作成したり、削除したりする処理
"""
from pyodide.ffi import JsProxy
from pyscript import document

def make_button(value: str, 
                func_name: str = "game.run", 
                text: str = None) -> JsProxy:
    """
    ボタンを作成する
    
    Args:
        value (str): ボタンに表示する文字列 / 選択するカードの番号
        func_name (str): 実行させる関数の名前
        text (str): 表示させる文字列

    Returns:
        JsProxy: ボタンのインスタンス
    """
    button = document.createElement('button')

    if text is None:
        text = value

    button.textContent = text
    button.value = value
    button.id = value
    button.style = "width:100px;height:50px"
    button.setAttribute("py-click", func_name)
    button.setAttribute("accesskey", text[0].lower())
    return button

class Buttons:
    """
    ボタンを作成したり、削除したりする
    """
    def __init__(self, id_name: str = "#buttons"):
        """
        Attributes:
            buttons_area (JsProxy): ボタンを表示させるエリア
            
        Args:
            id_name (str): HTML 上のボタンを設置するための場所の情報
        """
        self.buttons_area = document.querySelector(id_name)
        self.buttons = []

    def make(self, 
             card_num: int = 1,
             value: str = None,
             text: str = None, 
             func_name: str = "game.run") -> None:
        """
        ボタンの作成
        
        Args:
            card_num (int): 選択するカードの番号
            value (str): ボタンに持たせる情報
            text (str): ボタンに表示させる文字列
            func_name (str): 実行する関数名
            
        """
        is_value_none = value is None
        is_text_none = text is None

        for i in range(card_num):
            if is_value_none:
                value = str(i)
            if is_text_none:
                text = str(i)

            button = make_button(value, text = text, func_name = func_name)
            self.buttons_area.appendChild(button)
            self.buttons.append(button)

    def delete(self) -> None:
        """
        ボタンの削除
        """
        for b in self.buttons:
            self.buttons_area.removeChild(b)
        self.buttons = []