from pathlib import Path
import sys

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Field,
)

def test_field():
    """
    フィールドクラスのテスト
    """
    field = Field()
    print(field)

    