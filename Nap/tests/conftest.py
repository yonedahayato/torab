from pathlib import Path
import pytest

FILE_DIR = Path(__file__).parent.absolute()

@pytest.fixture
def data_dir() -> str:
    """
    テストの結果出力などに使うディレクトリの参照
    
    Returns:
        str: データディレクトリのパス
    """
    _data_dir = FILE_DIR / "data"
    _data_dir.mkdir(exist_ok=True)
    return str(_data_dir)