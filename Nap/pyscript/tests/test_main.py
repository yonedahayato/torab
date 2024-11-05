"""
pyscript で実行するメインスレッドの処理のテスト

Note:
    https://qiita.com/skokado/items/0061c608ecad733579a1
"""

from bs4 import BeautifulSoup
from http.server import HTTPServer
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_display_version(http_server: HTTPServer):
    url = http_server

    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver=driver, timeout=10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[py-click]")))
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")
    target_id = "python-version"
    target_element = soup.find(id=target_id)

    if target_element:
        target_text = target_element.get_text()
        print(f"ID '{target_id}' のテキスト: {target_text}")
        assert "3.11.3" in target_text

    else:
        raise Exception(f"ID '{target_id}' が見つかりませんでした。")        
