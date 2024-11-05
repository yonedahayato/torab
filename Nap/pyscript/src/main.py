"""
pyscript の main thread で動作する処理
main() を実行しているため、他の python file からの参照は非推奨
"""

import pandas as pd
from pyscript import document
import pydantic
import sys

def display_version() -> None:
    """
    python の version を表示する
    """
    versions = {
        "#python-version": sys.version,
        "#pydantic-version": f"pydantic: {pydantic.__version__}",
        "#pandas-version": f"pandas: {pd.__version__}",
    }
    for tag_id, version_text in versions.items():
        info_version = document.querySelector(tag_id)
        info_version.innerText = version_text
    
def main():
    """
    main thred で実行する処理が実行される
    """
    display_version()

main()