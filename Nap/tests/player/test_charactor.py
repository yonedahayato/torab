import pytest

from src.player import (
    Takeshi,
    Shizuka,
)

class TestTakeshi:
    """
    Takeshi のテスト
    """
    def test_talk(self):
        """
        talk メソッドのテスト
        """
        takeshi = Takeshi()
        assert takeshi.talk("introduction") == "俺の名前は、たけし！"
        assert takeshi.talk("favorite") == "好きなスートは、クラブさ！"
        assert takeshi.talk("rule") == "ハンデとして手札のスートを一枚だけ教えてやるよ！"
        assert takeshi.talk("conversation_1") == "むむむ！"
        assert takeshi.talk("conversation_2") == "お前！やるな！"

class TestShizuka:
    """
    Shizuka のテスト
    """
    def test_talk(self):
        """
        talk メソッドのテスト
        """
        shizuka = Shizuka()
        assert shizuka.talk("introduction") == "私の名前は、しずか！"
        assert shizuka.talk("favorite") == "好きなスートは、ハート！"
        assert shizuka.talk("rule") == "ハンデとして手札の数字を一枚だけ教える"
        assert shizuka.talk("conversation_1") == "なるほど！"
        assert shizuka.talk("conversation_2") == "君！なかなかね！"

