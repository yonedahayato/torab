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

def read_image(
        image_path: str,
        is_white_padding: bool = True,
        ) -> np.ndarray:
    """
    png の画像を opencv で読み込み、背景を白塗りする

    Args:
        image_path (str): 画像のパス
    """
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image.shape[2] == 4 and is_white_padding:
        # 透過部分の確認
        index = np.where(image[:, :, 3] == 0)

        # 透過部分の白塗り
        image[index] = [255, 255, 255, 255]

        # アルファチャネルの削除
        image = np.delete(image, 3, axis=2)

    return image

def draw_mark(mark: str, card_image: np.ndarray) -> np.ndarray:
    """
    カードにマークの情報を記載

    Args:
        mark (str): 表示するマーク
        card_image (np.ndarray): 表示するカードの画像

    Returns:
        np.ndarray: 記載したカードの画像
    """
    if mark == "♣":
        mark_image_path = CARD_IMAGE_DIR / "club.png"
    elif mark == "♠":
        mark_image_path = CARD_IMAGE_DIR / "club.png"
    elif mark == "♥":
        mark_image_path = CARD_IMAGE_DIR / "club.png"
    elif mark == "♦":
        mark_image_path = CARD_IMAGE_DIR / "club.png"
    else:
        return card_image

    mark_image = read_image(mark_image_path, is_white_padding=False)
    mark_image_size = min(int(card_image.shape[0] * 0.8), int(card_image.shape[1] * 0.8))
    mark_image = cv2.resize(mark_image, (mark_image_size, mark_image_size))

    offset = int(card_image.shape[0] * 0.07)
    x1, y1, x2, y2 = offset, offset, mark_image.shape[1] + offset, mark_image.shape[0] + offset
    card_image[y1:y2, x1:x2] = card_image[y1:y2, x1:x2] * (1 - mark_image[:, :, 3:] / 255) + \
                mark_image[:, :, :3] * (mark_image[:, :, 3:] / 255)

    return card_image

def draw_number(num: int, card_image: np.ndarray) -> np.ndarray:
    """
    カードに数字の情報を記載

    Args:
        num (int): 表示するマーク
        card_image (np.ndarray): 表示するカードの画像

    Returns:
        np.ndarray: 記載したカードの画像
    """
    card_image = cv2.putText(card_image, str(num), (25, 130), cv2.FONT_HERSHEY_DUPLEX, 3.0, (0, 0, 0), 4)

    return card_image

class CardButton(ToggleButtonBehavior, Image):
    """
    カードのボタン
    """
    def __init__(self, **kwargs: dict):
        self.is_available = kwargs.pop("is_available", None)
        self.run_func = kwargs.pop("run_func", None)
        self.card_id = kwargs.pop("card_id", None)
        self.text = kwargs.pop("text", None)

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

        if self.text:
            # テキストの情報があれば、手札のマークなどの情報を表示する
            image = draw_mark(self.text, image)

        if isinstance(self.text, int):
            image = draw_number(self.text, image)

        # 上下反転
        buf = cv2.flip(image, 0)

        # opencv は bgr 構造のため、それを明示
        image_texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        # image_texture.blit_buffer(buf.tostring(), colorfmt='bgr', bufferfmt='ubyte')
        image_texture.blit_buffer(buf.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

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
    message_area = ObjectProperty(None)
    talk_area = ObjectProperty(None)
    progress_button = ProgressButton()

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.game_buttons = {}
        self.charactor_images = []

        self.start()
        self.hands_areas = {}
        self.field_cards = {}
        self.info_area = None

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

    def set_hands_area(self, 
                       players: list[Player],
                       can_play: bool,
                       ) -> None:
        """
        各プレイヤーの手札を表示する場所を決定し、表示する

        Args:
            players (list[Player]): プレイヤーの集合
            can_play (bool):
                True: カードを選択する場面 / False: カードを選択する場面でない

        Note:
            参加しているプレイヤーの数によって、cpu のプレイヤーの場所は変わる
        """
        for player in players:
            hand_area = self.hands_areas.get(str(player), None)

            if hand_area:
                # すでに手札が表示されているなら削除する
                self.remove_widget(hand_area)

            if player.cpu:
                # cpu の手札を表示する
                hands = player.show_hand()
                # pos = [self.width * 0.5, - self.height * 0.3]
                # pos = [self.width * 0.5, - self.height * 0.55]
                pos_hint = {'x': 0.37, 'y': 0.67}
                size_hint = [0.3, 0.3]
            else:
                hands = player.cards
                # pos = [self.root.width * 0.5, - self.root.height * 0.55]
                # pos = [self.width * 0.5, - self.height * 0.55]
                pos_hint = {'x': 0.25, 'y': -0.25}
                size_hint = [0.5, 0.5]

            # 表示するエリアを決定
            hands_area = HandGrid(cols=len(hands), spacing=10, size_hint=size_hint, pos_hint=pos_hint)
            hands_area.bind(minimum_height=hands_area.setter('height'))
            # todo: ハンドを表示する位置やサイズを決定する

            hands_area = self.set_each_hands(hands, hands_area, can_play=can_play, is_cpu=player.cpu)

            self.add_widget(hands_area)
            self.hands_areas[str(player)] = hands_area

    def set_each_hands(self, 
                  hands: list, 
                  hands_area: HandGrid,
                  is_cpu: bool,
                  can_play: bool = False,
                  disables: list[bool] = None,
                  ) -> None:
        """
        手札のカードを表示する

        Args:
            hands (list): ハンドのカード
            hands_area: ハンドを表示するエリア
            is_cpu (bool): 表示するハンドがcpuのものかどうか

            can_play (bool): 下の1の状況下どうか
                True: カードを選択する場面 / False: カードを選択する場面でない
            disables (list[bool]): カードごとに、提出できるカードかどうかが格納されたリスト

        Note:
            カードのボタンが反応しない状況は2つ
                1. カードは配ってあるが、ゲームが始まっていないなどの、カードを選択する場面でない
                2. カードを選択する場面であるが、提出できないカードである
        """

        # None の場合は、すべて、実行可能な状態にする
        if disables is None:
            disables = [True] * len(hands)

        for card_id, (card_tmp, disable) in enumerate(zip(hands, disables, strict=True)):
            
            if is_cpu:
                if card_tmp != "?":
                    text = card_tmp.split("-")[0]
                else:
                    text = None
                # cpu のカードを表示
                card_button = CardButton(
                    source=str(CARD_IMAGE_DIR / "back.png"),
                    is_available=False,
                    run_func=None,
                    card_id=card_id,
                    text=text
                )
                card_button.size = [300, 300]
            else:
                # ユーザのカードを表示

                # ボタンを実行可能な状態にするかどうか
                is_available = (can_play and disable)

                # ユーザのカードを表示
                card_button = CardButton(source=str(CARD_IMAGE_DIR / card_tmp.image_path.name), 
                                        is_available=is_available,
                                        run_func=self.run,
                                        card_id=card_id)
                card_button.size = [300, 300]

            hands_area.add_widget(card_button)

        return hands_area

    def set_info(self, field: Field):
        """
        フィールドの情報を表示する

        Args:
            field (Field): フィールド
        """

        if self.info_area is not None:
            self.remove_widget(self.info_area)

        pos_hint = {'x': 0.2, 'y': 0.3}
        size_hint = [0.3, 0.3]
        self.info_area = HandGrid(cols=3, spacing=10, size_hint=size_hint, pos_hint=pos_hint)

        # 山札の表示
        deck = CardButton(
            source=str(CARD_IMAGE_DIR / "back.png"),
            is_available=False,
            run_func=None,
            card_id=0,
            text=len(field.deck)
        )
        deck.size = [200, 200]
        self.info_area.add_widget(deck)

        # 捨て札の表示
        trash = CardButton(
            source=str(CARD_IMAGE_DIR / "trash.png"),
            is_available=False,
            run_func=None,
            card_id=0,
            text=len(field.trash)
        )
        trash.size = [150, 150]
        self.info_area.add_widget(trash)

        trump = CardButton(
            source=str(CARD_IMAGE_DIR / "blue_back.png"),
            is_available=False,
            run_func=None,
            card_id=0,
            text=field.trump.mark
        )
        trump.size = [200, 200]
        self.info_area.add_widget(trump)

        self.add_widget(self.info_area)

    def set_field_cards(self, field: Field) -> None:
        """
        出したカードを表示する

        Args:
            field (Field): フィールド
        """
        self.delete_field_cards()

        for card_id, player in enumerate(field.players):
            card = field.cards.get(str(player), None)

            if card is None:
                continue

            if player.cpu:
                pos_hint = {'x': 0.45, 'y': 0.6}
            else:
                pos_hint = {'x': 0.45, 'y': 0.3}

            card_button = CardButton(
                source=str(CARD_IMAGE_DIR / card.image_path.name),
                is_available=False,
                run_func=None,
                card_id=card_id,
                text=None,
            )
            card_button.pos_hint = pos_hint
            card_button.size_hint = [0.1, 0.1]
            self.field_cards[str(player)] = card_button
            self.add_widget(card_button)

    def delete_field_cards(self):
        """
        出したカードを削除する
        """
        for card in self.field_cards.values():
            self.remove_widget(card)

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

        # cpu のキャラクターを表示する
        self.set_charactors(cpus)

        # cpu と ユーザのカードを表示
        self.set_hands_area(field.players, can_play)

        # 山札、捨て札、場、切り札などの情報を表示する
        self.set_info(field)

        if len(field.cards) == 0:
            # 場のカードがなければ、表示されているカードを削除する
            self.delete_field_cards()
        else:
            # 出したカードを表示する
            self.set_field_cards(field)

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

        # 画面上にある不要なものを削除
        for charactor_image in self.charactor_images:
            self.remove_widget(charactor_image)

        self.delete_field_cards()
        self.delete_go_button()
        self.remove_widget(self.info_area)

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
        self.game = game_class(
            self.delete_go_button, 
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