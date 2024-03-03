import sys
from pathlib import Path

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from utils import (
    Suit,
)
from player import (
    Declear,
)

def test_declear():
    """Test declear.
    宣言のテスト
    """
    declear = Declear(num=13, suit=Suit.club)

if __name__ == '__main__':
    test_declear()