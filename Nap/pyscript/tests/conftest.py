from http.server import (
    HTTPServer as SuperHTTPServer,
    SimpleHTTPRequestHandler
)
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import threading

class HTTPServer(SuperHTTPServer):
    """
    ThreadでSimpleHTTPServerを動かすためのラッパー用Class.
    Ctrl + Cで終了されるとThreadだけが死んで残る.
    KeyboardInterruptはpassする.
    """
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()

@pytest.fixture()
def http_server():
    """
    サーバを立てて、url を返す
    """
    host, port = '127.0.0.1', 8888
    url = f'http://{host}:{port}/index.html'
    # serve_forever をスレッド下で実行
    server = HTTPServer((host, port), SimpleHTTPRequestHandler)
    thread = threading.Thread(None, server.run)
    thread.start()
    yield url  # ここでテストに遷移
    # スレッドを終了
    server.shutdown()
    thread.join()

@pytest.fixture()
def driver(http_server: HTTPServer) -> webdriver.Chrome:
    """
    driver
    """
    url = http_server

    driver = webdriver.Chrome()
    driver.get(url)
    wait = WebDriverWait(driver=driver, timeout=10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[py-click]")))

    yield driver
    driver.quit()

@pytest.fixture()
def html(driver: webdriver.Chrome) -> str:
    """
    url から html を取得
    """
    html = driver.page_source

    return html