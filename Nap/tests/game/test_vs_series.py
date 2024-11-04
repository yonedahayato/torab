from pathlib import Path
import pytest
import sys

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.game import (
    VSBase
)

class TestVSBase:
    """
    VSBase クラスのテスト
    """
    def test_raise_set_player(self):
        """
        VSBase クラスをインスンス化して、_set_player method を実行して、NotImplementedErrorを確認する
        """
        with pytest.raises(NotImplementedError):
            VSBase()._set_player()