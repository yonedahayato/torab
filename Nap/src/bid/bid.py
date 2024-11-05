from enum import IntEnum
import pandas as pd
import random

from ..player import (
    Player,
)

from ..field import (
    Field,
)

class NapDeclaration:
    """
    ナップのゲームにおける宣言
    """
    table = pd.DataFrame.from_records([
        ["pass", -1, "宣言なし", 0, 0],
        ["no_declare", 0, "未宣言", 0, 0],
        ["two", 1, "2トリック以上勝つ", 2, -2],
        ["three", 2, "3トリック以上勝つ", 3, -3],
        ["misere", 3, "全トリック負ける", 3, -3],
        ["four", 4, "4トリック以上勝つ", 4, -4],
        ["nap", 5, "全トリック勝つ", 10, -6],
        ["wellington", 6, "全トリック勝つ", 20, -12]
    ], 
    columns=["name", "d_value", "description", "success_point", "failure_point"])

    def __init__(self, name: str = "no_declare"):
        if name not in self.table["name"].values:
            raise ValueError(f"NapDeclaration において、異常なビッド: {name}")
        
        self.name = name

    def __repr__(self):
        return f"NapDeclaration(name={self.name})"
    
    def is_pass(self):
        """
        パスをしたかどうか
        """
        return self.name == "pass"
    
    def is_declared(self):
        """
        宣言を一度でもしたかどうか
        """
        return self.name != "no_declare"

class NapBid:
    """
    ナップのゲームにおけるビッドの進行を管理する
    """
    def __init__(self, field: Field):
        """
        ビッドの準備

        Note:
            最初に宣言するプレイヤーはランダム            
        """
        self.field = field
        print(self.field)
        self.declarations = {p.name: NapDeclaration("no_declare") for p in self.field.players}
        print(self.declarations)

        self.start_bit_player_id = random.randint(0, len(self.field.players)-1)
        self.is_finish_flag = False
        self.bid_cnt = 0
        self.declarer = None
        self.invalid = False

    def __iter__(self):
        return self

    def __next__(self):
        """
        プレイヤー 1分のビッドの処理

        Note:
            処理の流れ
                1. ビッドを行うプレイヤーを決定
                2. 宣言
                3. 宣言を格納
                4. bid_cnt をインクリメント
        """
        if self.is_finish_flag:
            raise StopIteration

        player_id = (self.start_bit_player_id + self.bid_cnt) % len(self.field.players)
        player = self.field.players[player_id]
        declaration = self.declarations.get(player.name)

        if not declaration.is_pass():
            declarable_list = declaration.get_declarable_list()
            new_declaration = self.bid(player, declarable_list)
            self.declarations[player.name] = new_declaration

        if self.is_finish():
            self.is_finish_flag = True
            self.declarer = player

        if self.is_everyone_pass():
            self.is_finish_flag = True
            self.invalid = True

        # closing
        self.bid_cnt += 1
        return self.field
    
    def is_everyone_pass(self):
        """
        全員パスをしている状態かどうか
        """
        pass_cnt = 0
        for d in self.declarations.values():
            if d.is_pass():
                pass_cnt += 1

        return pass_cnt == len(self.declarations)

    def is_finish(self):
        """
        終わったかどうかの判定を行う

        Note:
            1 人以外、pass であれば、終了
        """
        pass_cnt = 0
        declared_cnt = 0
        for d in self.declarations.values():
            if d.is_pass():
                pass_cnt += 1
            if d.is_declared():
                declared_cnt += 1

        return pass_cnt == (len(self.declarations) - 1) and \
               declared_cnt == (len(self.declarations))
    
    def bid(self, player: Player):
        """
        """
        card = player.play_card()
            
        return card
