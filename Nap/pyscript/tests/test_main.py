"""
pyscript で実行するメインスレッドの処理のテスト

Note:
    https://qiita.com/skokado/items/0061c608ecad733579a1
"""

from bs4 import BeautifulSoup
from http.server import HTTPServer
import requests

def test_display_version(http_server: HTTPServer):
    url = http_server
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    target_id = "info-version"
    target_element = soup.find(id=target_id)
    if target_element:
        target_text = target_element.get_text()
        print(f"ID '{target_id}' のテキスト: {target_text}")
    else:
        print(f"ID '{target_id}' が見つかりませんでした。")
    assert response.text == '<html>Hello pytest!</html>'
