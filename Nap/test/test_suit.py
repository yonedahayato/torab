import sys
from pathlib import Path

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from utils import (
    Suit,
)

def test_suit():
    """Test suit.
    スートのテスト
    """
    spade = Suit.spade
    heart = Suit.heart
    diamond = Suit.diamond
    club = Suit.club

    # spade
    assert spade == spade
    assert spade > heart
    assert spade > diamond
    assert spade > club
    
    # heart
    assert heart < spade
    assert heart == heart
    assert heart > diamond
    assert heart > club
    
    # diamond
    assert diamond < spade
    assert diamond < heart
    assert diamond == diamond
    assert diamond > club
    
    # club
    assert club < spade
    assert club < heart
    assert club < diamond
    assert club == club

if __name__ == '__main__':
    test_suit()