from pathlib import Path
import sys

FILE_DIR = Path(__file__).parent.absolute()
PROJECT_DIR = FILE_DIR.parent.parent.absolute()
sys.path.append(str(PROJECT_DIR))

from src.utils import (
    Field,
)

def test_field(data_dir):
    """
    フィールドクラスのテスト
    
    Args:
        data_dir (str): 結果を出力するためのディレクトリ
    """
    field = Field()
    print(field)
    image_path = Path(data_dir) / "test_field.jpg"
    field.make_image(save_path=image_path)