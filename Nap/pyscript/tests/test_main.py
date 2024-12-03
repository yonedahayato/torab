"""
pyscript で実行するメインスレッドの処理のテスト

Note:
    https://qiita.com/skokado/items/0061c608ecad733579a1
"""

from bs4 import BeautifulSoup

def test_display_version(html: str):
    """
    pyscript で表示した情報を確認する

    Args:
        http_server (HTTPServer): テストサーバ
    """

    soup = BeautifulSoup(html, "html.parser")
    target_id = "python-version"
    target_element = soup.find(id=target_id)

    if target_element:
        target_text = target_element.get_text()
        print(f"ID '{target_id}' のテキスト: {target_text}")
        assert "3.11.3" in target_text

    else:
        raise Exception(f"ID '{target_id}' が見つかりませんでした。")