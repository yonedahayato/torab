"""
pyscript の main thread で動作する処理
main() を実行しているため、他の python file からの参照は非推奨
"""

from pyscript import document
import sys

sys.path.append("/home/work")

def display_version() -> None:
    """
    python の version を表示する
    """
    info_version = document.querySelector("#info-version")
    info_version.innerText = sys.version
    
def main():
    """
    main thred で実行する処理が実行される
    """
    display_version()

main()