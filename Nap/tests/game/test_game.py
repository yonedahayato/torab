import io
from pathlib import Path
import sys

from _pytest.monkeypatch import MonkeyPatch

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.game import SimpleNapVSTakeshi

class TestSimpleNapVSTakeshi:
    """
    Simple Game class のテスト
    """
    def test_game(self, monkeypatch: MonkeyPatch):
        """
        ゲームの実行のテスト
        
        Args:
            monkeypatch (MonkeyPatch): pytest tool
        """
        monkeypatch.setattr('sys.stdin', io.StringIO("0\n0\n0\n"))
        game = SimpleNapVSTakeshi()
        game.play()
