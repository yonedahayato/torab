import js
# from pyscript import window, document
import pyodide
from pyodide.ffi import create_proxy
from PIL import Image
import io
import json
import base64

def run(event: pyodide.ffi.JsProxy):
    """
    必要な情報を取得し、画像処理の実行を行う
    """

    # 入力画像の取得
    file_input = js.document.querySelector('#imageInput')
    file = file_input.value
    if not file:
        print("画像をアップロードしてください。")
        return
    
    # 新しいサイズの取得
    # new_width = int(js.document.getElementById('widthInput').value)
    # new_height = int(js.document.getElementById('heightInput').value)
    # if new_width <= 0 or new_height <= 0:
    #     print("幅と高さは正の整数を入力してください。")
    #     return
    
    size_aspect = js.document.getElementById("size_aspect").value
    size_aspect = json.loads(size_aspect)
    aspect = size_aspect["h"] / size_aspect["w"]

    upper_rate = int(js.document.getElementById('upperRate').value)
    
    # FileReaderを使用してファイルを読み込む
    reader = js.FileReader.new()

    for f in file_input.files:
        reader.readAsArrayBuffer(f)
        break
    
    def on_load(event: pyodide.ffi.JsProxy):
        """
        変換処理のボタンが押された時の処理
        """
        buffer = event.target.result
        image_byte = buffer.to_bytes()
        image = Image.open(io.BytesIO(image_byte))
        print(f"image size {image.size}")
        # width, height = image.size

        # 画像処理
        # new_image = image.resize((new_width, new_height))
        new_image = padding(image, (0, 0, 0), aspect, upper_rate)

        # 画像をbase64エンコードされた文字列に変換
        buffered = io.BytesIO()
        new_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # 出力画像を表示
        output_image = js.document.getElementById('outputImage')
        output_image.src = f"data:image/png;base64,{img_str}"
    
    reader.onload = create_proxy(on_load)

def padding(pil_img, background_color, aspect, upper_rate):
    """
    枠を埋める処理
    """
    width, height = pil_img.size
    target_height = int(width * aspect)
    target_width = int(height / aspect)
    # height = target_height

    if target_height == height:
        return pil_img
    elif target_height > height:
        result = Image.new(pil_img.mode, (width, target_height), background_color)
        pad_size = int((target_height - height) * upper_rate / 10)
        result.paste(pil_img, (0, pad_size))
        return result
    else:
        result = Image.new(pil_img.mode, (target_width, height), background_color)
        result.paste(pil_img, ((target_width - width) // 2, 0))
        return result