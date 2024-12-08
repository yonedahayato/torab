import cv2
import japanize_kivy
import numpy as np

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty,
)
from kivy.uix.behaviors import (
    ButtonBehavior,
    ToggleButtonBehavior,
)
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
)
from kivy.uix.widget import Widget

from pathlib import Path
import sys

BASE_DIR = Path(__file__).parents[2]
sys.path.append(str(BASE_DIR))

from src.field import (
    Field,
)
from src.player import (
    Player,
)

from Kivy.src.utils.games import (
    GUIGameBase,
    VSTakeshiGUIGame,
)

KV_DIR = BASE_DIR / "kivy/asset/kv"
Builder.load_file(str(KV_DIR / "main.kv"))

RESOURCE_DIR = BASE_DIR / "asset/image"
CARD_IMAGE_DIR = RESOURCE_DIR / "cards/png"

def read_image(image_path: str) -> np.ndarray:
    """
    png の画像を opencv で読み込み、背景を白塗りする
    """
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4:
        # 透過部分の確認
        index = np.where(image[:, :, 3] == 0)

        # 透過部分の白塗り
        image[index] = [255, 255, 255, 255]

        # アルファチャネルの削除
        image = np.delete(image, 3, axis=2)

    return image

class CardButton(ToggleButtonBehavior, Image):
    """
    カードのボタン
    """
    def __init__(self, **kwargs: dict):
        self.is_available = kwargs.pop("is_available", None)
        self.run_func = kwargs.pop("run_func", None)
        self.card_id = kwargs.pop("card_id", None)

        super().__init__(**kwargs)
        self.souce = kwargs["source"]

        # 画像を編集できるようにテクスチャーとして扱う
        self.texture = self.button_texture(self.souce)

    def on_state(self, widget, value) -> None:
        """
        トグルボタンの状態、状態によって画像が変化させる
        """

        is_off = (value == "down") and self.is_available
        self.texture = self.button_texture(self.souce, off=is_off)

    def button_texture(self, data: str, off: bool = False) -> None:
        """
        画像を変化させる、押した状態の時に矩形+色を暗く

        Args:
            data (str): 画像パス
            off (bool): 画像が、選択状態かどうか
        """
        image = read_image(data)

        if off:
            image = cv2.rectangle(image, (2, 2), (image.shape[1]-2, image.shape[0]-2), (255, 255, 0), 10)

        # 上下反転
        buf = cv2.flip(image, 0)
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')

        return image_texture

    def on_press(self):
        """
        押した時の処理
        """
        if self.is_available:
            self.pos = [self.pos[0], self.pos[1] + 10]

    def on_release(self):
        """
        離した時の処理
        """
        if self.is_available:
            self.pos = [self.pos[0], self.pos[1] - 10]
            self.run_func(card_id = self.card_id)

class HandGrid(GridLayout):
    """
    ハンドを表示する
    """

class CharactorImage(Image):
    """
    キャラクターの画像
    """

class ProgressButton(Button):
    """
    ゲームの進行を行うためのボタン
    """
    def __init__(self, **kwargs: dict):
        """
        Note:
            pop method により入力情報から削除
        """
        self.next_action = kwargs.pop("next_action", None)
        super().__init__(**kwargs)

class GameSelectButton(Button):
    """
    ゲームを選択するためのボタン
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.game_name = kwargs["text"]

GAMES = {
    "VS Takeshi Lv.1": VSTakeshiGUIGame,
}

class GameScreen(Screen):
    """
    ゲームの進行について
    """
    info_area = ObjectProperty(None)
    message_area = ObjectProperty(None)
    talk_area = ObjectProperty(None)
    progress_button = ProgressButton()

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.game_buttons = {}
        self.charactor_images = []

        self.start()
        self.hands_box = None

    def set_image_path(self,
                       object: ObjectProperty,
                       image_path: str) -> ObjectProperty:
        """
        画像のパスを設定する
        """

        object.source = str(image_path)
        return object

    def set_card(self, 
                 object: ObjectProperty,
                 image_name : str ="2_of_clubs.png",
                 ) -> ObjectProperty:
        """
        カードの画像を設定する
        """

        image_path = str(CARD_IMAGE_DIR / image_name)
        card_object = self.set_image_path(object, image_path)
        card_object.size = [300, 300]

        return card_object

    def set_charactors(self, charactors: list[Player]):
        """
        キャラクター達の表示
        """
        for charactor in charactors:
            self.charactor_image = CharactorImage()
            self.charactor_image = self.set_image_path(self.charactor_image, charactor.image_path())
            self.charactor_image.size = [200, 200]

            self.charactor_images.append(self.charactor_image)
            self.add_widget(self.charactor_image)

    def set_hands(self, 
                  hands: list, 
                  can_play: bool = False,
                  disables: list[bool] = None):
        """
        手札のカードを表示する

        Args:
            hands (list): ハンドのカード
            can_play (bool): 下の1の状況下どうか
                True: カードを選択する場面 / False: カードを選択する場面でない
            disables (list[bool]): カードごとに、提出できるカードかどうかが格納されたリスト

        Note:
            カードのボタンが反応しない状況は2つ
                1. カードは配ってあるが、ゲームが始まっていないなどの、カードを選択する場面でない
                2. カードを選択する場面であるが、提出できないカードである
        """
        if self.hands_box:
            # すでに手札があるなが削除する
            self.remove_widget(self.hands_box)

        self.hands_box = HandGrid(cols=len(hands), spacing=10, size_hint_y=None)
        self.hands_box.bind(minimum_height=self.hands_box.setter('height'))

        if disables is None:
            disables = [True] * len(hands)

        for card_id, (card_tmp, disable) in enumerate(zip(hands, disables, strict=True)):
            # self.card_button = self.set_card(self.card_button, str(card_tmp.image_path.name))
            is_available = can_play and disable
            card_button = CardButton(source=str(CARD_IMAGE_DIR / card_tmp.image_path.name), 
                                     is_available=is_available, 
                                     run_func=self.run,
                                     card_id = card_id)
            card_button.size = [300, 300]
            self.hands_box.add_widget(card_button)

        self.add_widget(self.hands_box)

    def set_info(self, field: Field):
        """
        フィールドの情報を表示する
        """
        targets = {
            "山札" : len(field.deck), 
            "捨て札" : len(field.trash),
            "場" : len(field.cards),
            }
        
        if field._trump:
            targets["切り札"] = field.trump.mark

        output_text = ""
        for key, value in targets.items():
            if key == "場" and value != 0:
                output_text += "場 : \n"
                for player, card in field.cards.items():
                    output_text += f"    {player}: {str(card)}\n"
            else:
                output_text += f"{key} : {value}\n"

        self.info_area.text = output_text

    def set_message(self, message: str, charactor_name: str = None) -> None:
        """
        メッセージを表示する
        """
        self.message_area.text = message

    def set_talk(self, message: str, charactor_name: str = None) -> None:
        """
        キャラクターの吹き出しを表示する
        """
        self.talk_area.text = message

    def set_field(self, field: Field, can_play: bool = False):
        """
        field の情報を画面に表示する

        Args:
            field (Field): フィールド
            can_play (bool): プレイを行う状況かどうか
        """
        # プレイヤーの情報を表示
        cpus = [p for p in field.players if p.cpu]
        user = [p for p in field.players if not p.cpu][0]

        # cpu は、キャラクターを表示する
        self.set_charactors(cpus)

        # ユーザは、カードを表示する
        self.set_hands(user.cards, can_play)

        # 山札、捨て札、場、切り札などの情報を表示する
        self.set_info(field)

        # message を表示する
        self.set_message(field.message_log[-1])

    def make_go_button(self, 
                       next_action: str = "talk") -> None:
        """
        progress button を作成
        """
        self.progress_button = ProgressButton(next_action=next_action)
        self.progress_button.bind(on_press=self.go)
        self.add_widget(self.progress_button)

    def delete_go_button(self) -> None:
        """
        progress button を削除
        """
        self.progress_button.opacity = 0
        self.progress_button.disabled = True

    def start(self):
        """
        ゲームの選択する画面を作成する
        
        Note:
            選択するボタンを作成する
        """
        self.message_area.text = "ゲームを選択してください"
        for game_name in GAMES.keys():
            game_button = GameSelectButton(text=game_name)
            game_button.bind(on_press=self.select)

            self.game_buttons[game_name] = game_button
            self.add_widget(game_button)

    def restart(self) -> None:
        """
        ゲームを選択する画面を整え、再度ゲームを選択させる
        """
        self.talk_area.text = ""
        self.info_area.text = ""

        for charactor_image in self.charactor_images:
            self.remove_widget(charactor_image)
        self.delete_go_button()

        self.start()
        # self.describe_area.removeChild(self.ul_tag)

    def select(self, btn: GameSelectButton) -> None:
        """
        選択されたゲームを実行する

        Note:
            ボタンを削除する
            次のアクションは、talk
        """
        # ゲーム名の取得
        game_name = btn.game_name

        game_class = GAMES.get(game_name, None)
        if game_class is None:
            raise Exception("ゲームの選択に失敗")

        # ゲーム決定
        self.game = game_class(self.delete_go_button, 
                               self.make_go_button,
                               self.set_message,
                               self.set_field,
                               self.set_talk,
                               )
        self.set_field(self.game.field)

        # ゲームのタイトルと説明を表示
        # self.describe(game_name, game_class.describe)

        # ゲーム選択の button を削除
        for game_button in self.game_buttons.values():
            game_button.opacity = 0
            game_button.disabled = True

    def go(self, btn):
        """
        メッセージを読んだことがわかった後の処理        
        """
        next_action = btn.next_action

        if self.game.is_finish:
            self.restart()
        else:
            self.game.go(next_action)


    def run(self, card_id: int = None) -> None:
        """
        ゲームを実行する        
        """
        self.game.run(card_id)
        # self.feild_area.textContent = str(self.game.field)

        if self.game.is_finish:
            self.restart()

class GameApp(App):
    """
    このアプリの起動と設定
    """

    message_text_size_rate = 0.2
    def build(self) -> ScreenManager:
        """build method
        このアプリの起動時の処理
        """
        Window.fullscreen = "auto"
        # Window.fullscreen = True
        
        sm = ScreenManager()

        game_screen = GameScreen(name="game")
        sm.add_widget(game_screen)

        return sm

if __name__ == "__main__":
    GameApp().run()