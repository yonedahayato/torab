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

from src.utils import (
    Card,
)
from src.field import (
    Field,
)
from src.player import (
    Player,
)
from src.game import (
    SimpleNapVSTakeshi,
    EasyNapVSTakeshi,
    EasyNapVSShizuka,
    NapVSShizuka,
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
        super().__init__(**kwargs)
        self.souce = kwargs["source"]

        # 画像を編集できるようにテクスチャーとして扱う
        self.texture = self.button_texture(self.souce)

    def on_state(self, widget, value) -> None:
        """
        トグルボタンの状態、状態によって画像が変化させる
        """

        is_off = (value == "down")
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
        self.pos = [self.pos[0], self.pos[1] + 10]

    def on_release(self):
        """
        離した時の処理
        """
        self.pos = [self.pos[0], self.pos[1] - 10]

class CharactorImage(Image):
    """
    キャラクターの画像
    """

class ProgressButton(Button):
    """
    """

class GameScreen(Screen):
    """
    アプリの進行について
    """
    charactor_image = CharactorImage()
    info_area = ObjectProperty(None)
    message_area = ObjectProperty(None)

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
            self.charactor_image = self.set_image_path(self.charactor_image, charactor.image_path())
            self.charactor_image.size = [200, 200]

    def set_hands(self, hands: list):
        """
        手札のカードを表示する
        """
        box = GridLayout(cols=len(hands), spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        for card_tmp in hands:
            # self.card_button = self.set_card(self.card_button, str(card_tmp.image_path.name))
            card_button = CardButton(source=str(CARD_IMAGE_DIR / card_tmp.image_path.name))
            card_button.size = [300, 300]
            box.add_widget(card_button)

        self.add_widget(box)

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
            output_text += f"{key} : {value}\n"

        self.info_area.text = output_text

    def set_message(self, message: str) -> None:
        """
        メッセージを表示する
        """
        self.message_area.text = message

    def set_field(self, field: Field):
        """
        field の情報を画面に表示する
        """
        # プレイヤーの情報を表示
        cpus = [p for p in field.players if p.cpu]
        user = [p for p in field.players if not p.cpu][0]

        # cpu は、キャラクターを表示する
        self.set_charactors(cpus)

        # ユーザは、カードを表示する
        self.set_hands(user.cards)

        # 山札、捨て札、場、切り札などの情報を表示する
        self.set_info(field)

        # message を表示する
        self.set_message(field.message_log[-1])

    def set_game(self):
        """
        ゲームの設定
        """
        game = SimpleNapVSTakeshi()
        self.set_field(game.field)

class GameApp(App):
    """
    このアプリの起動と設定
    """

    message_text_size_rate = 0.2
    def build(self) -> ScreenManager:
        """build method
        このアプリの起動時の処理
        """
        Window.fullscreen = 'auto'
        
        sm = ScreenManager()

        game_screen = GameScreen(name="game")
        game_screen.set_game()
        sm.add_widget(game_screen)

        return sm

if __name__ == "__main__":
    GameApp().run()