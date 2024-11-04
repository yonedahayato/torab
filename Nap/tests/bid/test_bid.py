from pathlib import Path
import pytest
import sys

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.bid import (
    NapBid,
)

class TestNapBid:
    """
    NapBid class のテスト
    """
    def test_nap_bid(self):
        """
        NapBid class の実行のテスト
        """