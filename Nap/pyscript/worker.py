"""
pyscript における worker に動いてもらう処理
main() を直接実行しているため、他の python file から参照は非推奨
"""

import sys
sys.path.append("/home/work")

from src.game import SimpleNapVSTakeshi

def main():
    """
    ゲームを実行する
    """
    game = SimpleNapVSTakeshi()
    game.play()

main()