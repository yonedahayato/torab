import pytest
from http.server import (
    HTTPServer as SuperHTTPServer,
    SimpleHTTPRequestHandler
)
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