from enum import IntEnum
import pandas as pd
import random

from ..player import (
    Player,
)

from ..field import (
    Field,
)

class BaseDeclaration:
    def __eq__(self, other) -> bool:
        """Equal.
        宣言の強さが同じかどうか
        
        """
        return self.d_value == other.d_value
    
    def __gt__(self, other) -> bool:
        """Greater than.
        宣言の強さが他の宣言より強いかどうか
        """
        return self.d_value > other.d_value
    
    def __ge__(self, other) -> bool:
        """Greater than or equal.
        宣言の強さが他の宣言以上かどうか
        """
        return self.d_value >= other.d_value
    
    def __lt__(self, other) -> bool:
        """Less than.
        宣言の強さが他の宣言より弱いかどうか
        """
        return self.d_value < other.d_value
    
    def __le__(self, other) -> bool:
        """Less than or equal.
        宣言の強さが他の宣言以下かどうか
        """
        return self.d_value <= other.d_value

class NapDeclaration(BaseDeclaration):
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
        self.d_value = self.table.query(f"name == '{name}'")["d_value"].values[0]

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
    
    def get_declarable_list(self) -> list[any]:
        """
        自身のディクレアに対してコールできるディクレアの一覧を返す
        """
        declarable_list = [NapDeclaration("pass")]
        declarable_list += [NapDeclaration(d) for d in self.table.query(f"d_value > {self.d_value}")["name"].values]

        return declarable_list

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
        self.declarations = {p: NapDeclaration("no_declare") for p in self.field.players}
        print(self.declarations)

        self.start_bit_player_id = random.randint(0, len(self.field.players)-1)
        self.is_finish_flag = False
        self.bid_cnt = 0
        self.declarer = None
        self.invalid = False

    def __iter__(self):
        return self

    def __next__(self) -> Field:
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

        if self.bid_cnt == 0:
            self.best_declaration = NapDeclaration("no_declare")

        player_id = (self.start_bit_player_id + self.bid_cnt) % len(self.field.players)
        player = self.field.players[player_id]
        declaration = self.declarations.get(player)

        if declaration.is_pass():
            """
            前の宣言がパスであれば、宣言できない
            """
            self.field.message = f"{player} はすでにパスを宣言しているので、これ以上の宣言はできない"

            # closing
            self.bid_cnt += 1
            return self.field

        # 選択できる宣言は、最も強い宣言よりも強い宣言
        declarable_list = self.best_declaration.get_declarable_list()

        if len(declarable_list) == 1:
            """
            選択できる宣言がなければ、パス扱いとなる
            """
            new_declaration = NapDeclaration(name = "pass")
            self.field.message = f"{player} は {new_declaration} しか宣言できない"

        else:
            new_declaration = self.bid(player, declarable_list)
            self.field.message = f"{player} が {new_declaration} を宣言した"

        self.declarations[player] = new_declaration

        if not new_declaration.is_pass():
            self.best_declaration = new_declaration
            self.declarer = player

        if self.is_finish():
            self.is_finish_flag = True
            # self.field.message += f"{self.declarer} の{str(self.best_declaration)}宣言が有効です"

        if self.is_everyone_pass():
            self.is_finish_flag = True
            self.invalid = True
            # self.field.message += "全員のプレイヤーがパスを行いました"

        # closing
        self.bid_cnt += 1
        return self.field
    
    def is_everyone_pass(self) -> bool:
        """
        全員パスをしている状態かどうか
        """
        pass_cnt = 0
        for d in self.declarations.values():
            if d.is_pass():
                pass_cnt += 1

        return pass_cnt == len(self.declarations)

    def is_finish(self)  -> bool:
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
    
    def bid(self, 
            player: Player, 
            declarable_list: list[NapDeclaration]) -> NapDeclaration:
        """
        プレイヤーの宣言の処理
        """
        declaration = player.declare(declarable_list)
        return declaration