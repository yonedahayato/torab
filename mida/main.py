import js
from pyodide.ffi import create_proxy
from PIL import Image
import io
import base64

def resize_image():
    # 入力画像の取得
    file_input = js.document.getElementById('imageInput')
    file = file_input.files[0]
    
    if not file:
        print("画像をアップロードしてください。")
        return
    
    # 新しいサイズの取得
    new_width = int(js.document.getElementById('widthInput').value)
    new_height = int(js.document.getElementById('heightInput').value)
    
    if new_width <= 0 or new_height <= 0:
        print("幅と高さは正の整数を入力してください。")
        return
    
    # FileReaderを使用してファイルを読み込む
    reader = js.FileReader.new()
    reader.readAsArrayBuffer(file)
    
    def on_load(event):
        buffer = event.target.result
        image = Image.open(io.BytesIO(buffer))
        
        # 画像のリサイズ
        resized_image = image.resize((new_width, new_height))
        
        # 画像をbase64エンコードされた文字列に変換
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # 出力画像を表示
        output_image = js.document.getElementById('outputImage')
        output_image.src = f"data:image/png;base64,{img_str}"
    
    reader.onload = create_proxy(on_load)
