"""
pyscript の worker 上で terminal を実行するには、以下の設定が必要だったので、server.py を実装
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Embedder-Policy: require-corp
  Cross-Origin-Resource-Policy: cross-origin
"""

from http.server import BaseHTTPRequestHandler
import socketserver
import os

PORT = 8000
# カレントディレクトリを取得
CWD = os.getcwd()

class RequestHandler(BaseHTTPRequestHandler):
    """
    index.html へ接続するための、handler
    """
    def end_headers(self) -> None:
        """
        pyscript の worker 上で、terminal を動かすときに必要な設定
        """
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self) -> None:
        """
        get でアクセスされた時の処理

        Note
            index.html 以外のファイルにもアクセスできるように調整
        """
        # リクエストされたパスを取得
        path = self.path

        # パスが空の場合は index.html を返す
        if path == '/':
            path = '/index.html'

        # リクエストされたファイルのパスを作成
        file_path = os.path.join(CWD, path[1:])

        # ファイルが存在する場合
        if os.path.exists(file_path):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # ファイルの内容を読み込んで返す
            with open(file_path, 'rb') as f:
                content = f.read()
                self.wfile.write(content)

        # ファイルが存在しない場合
        else:
            self.send_error(404, 'File not found')

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()