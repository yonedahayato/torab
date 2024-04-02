from pathlib import Path
import sys

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.game import SimpleNapVSTakeshi

class TestSimpleNapVSTakeshi:
    """
    Simple Game class のテスト
    """
    def test_game(self):
        """
        """
        game = SimpleNapVSTakeshi()
        game.play()
