from pathlib import Path
import sys

filedir = Path(__file__).parent.absolute()
parentdir = filedir.parent.absolute()
sys.path.append(str(parentdir))

from src.utils import (
    Suit,
)

class TestSuit:
    """
    Suit class のテスト
    """
    def test_compare(self) -> None:
        """
        スートの強さの順番を確認する

        Note:
            Suit class は、Enum を継承している
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
        
    def test_mark(self) -> None:
        """
        スートのマークのテスト
        """
        spade = Suit.spade
        heart = Suit.heart
        diamond = Suit.diamond
        club = Suit.club
        
        assert spade.mark == "♠"
        assert heart.mark == "♥"
        assert diamond.mark == "♦"
        assert club.mark == "♣"
        
    def test_image_url(self):
        """
        スートの画像の url についてのテスト
        """
        spade = Suit.spade
        heart = Suit.heart
        diamond = Suit.diamond
        club = Suit.club

        assert spade.image_url == "https://docs.google.com/drawings/d/e/2PACX-1vShkEbM-bF8ZdFUUVDTsFPtamISa-TgR2_v26Bzf6f-ugqmt3Ry8Ncj59t3TIEK_Lumr4OoH5WSr7lG/pub?w=596&h=596"
        assert heart.image_url == "https://docs.google.com/drawings/d/e/2PACX-1vS4Y024nBwRGYfrQkJsvh0bsQhNiM8g-_-DMSY_tNslQ6b5noqpYZrQ2fnTQJ7bZiLhXjObDzGGJ1gk/pub?w=596&h=596"
        assert diamond.image_url == "https://docs.google.com/drawings/d/e/2PACX-1vQWHrseqkqz3Yb2On0NewQYzXvtNDxx99aKRHUw36S8XUn2AZ5hhohswUfiQH2bO18CzdF2gVJb_kPw/pub?w=596&h=596"
        assert club.image_url == "https://docs.google.com/drawings/d/e/2PACX-1vRhDX5xCJqqutdXbcfSZxunVzpktaaXClS-0245bLmYFYA5QyDqPyjMfhUFNW73h26kai7TJbAlRRsl/pub?w=596&h=596"
