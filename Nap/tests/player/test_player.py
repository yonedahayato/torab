import pytest

from src.player import (
    Player,
)

@pytest.fixture()
def cpu_player() -> Player:
    """
    CPU Player を準備する

    Returns:
        Player: CPU Player
    """
    return Player(cpu = True)

class TestPlayer:
    """
    Player class のテスト
    """
    def test_init(self):
        """
        プレイヤークラスの作成
        """
        player = Player()

    def test_check_cards_can_submit(self, cpu_player: Player):
        """
        check_cards_can_submit メソッドのテスト
        """
        cpu_player.check_cards_can_submit()