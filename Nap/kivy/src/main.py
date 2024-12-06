from collections.abc import Callable
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
import random
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
        self.is_available = kwargs.pop("is_available", None)
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

    # def set_next_action(self, next_action: str):
    #     """
    #     """
    #     self.next_action = next_action

class GameSelectButton(Button):
    """
    ゲームを選択するためのボタン
    """
    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.game_name = kwargs["text"]

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

        # self.card_buttons.make_card(cards = player.cards)
        self.display_field(self.field, can_play = True)

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
            self.next_track_on_browser()
        elif next_action == "talk":
            # しゃべることがないのに、トークはできない
            raise Exception(f"next action が異常: {next_action} / 喋れない")
        else:
            raise ValueError(f"next action が異常: {next_action}")

class VSTakeshiGUIGame(GUIGameBase, SimpleNapVSTakeshi):
    """
    SimpleNapVSTakeshiをGUIで実行するためのクラス
    """
    def __init__(self, 
                 delete_go_button: Callable,
                 make_go_button: Callable,
                 message_func: Callable,
                 set_field_func: Callable,
                 set_talk_func: Callable
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

GAMES = {
    "VS Takeshi Lv.1": VSTakeshiGUIGame,
}

class GameScreen(Screen):
    """
    ゲームの進行について
    """
    charactor_image = CharactorImage()
    info_area = ObjectProperty(None)
    message_area = ObjectProperty(None)
    talk_area = ObjectProperty(None)
    progress_button = ProgressButton()

    def __init__(self, **kwargs: dict):
        super().__init__(**kwargs)
        self.game_buttons = {}

        self.start()

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
        box = GridLayout(cols=len(hands), spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        if disables is None:
            disables = [True] * len(hands)
        for card_tmp, disable in zip(hands, disables, strict=True):
            # self.card_button = self.set_card(self.card_button, str(card_tmp.image_path.name))
            is_available = can_play and disable
            card_button = CardButton(source=str(CARD_IMAGE_DIR / card_tmp.image_path.name), 
                                     is_available=is_available)
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
        self.game.go(next_action)

        if self.game.is_finish:
            self.restart()

    def run(self) -> None:
        """
        ゲームを実行する        
        """
        self.game.run()
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
        Window.fullscreen = 'auto'
        
        sm = ScreenManager()

        game_screen = GameScreen(name="game")
        sm.add_widget(game_screen)

        return sm

if __name__ == "__main__":
    GameApp().run()