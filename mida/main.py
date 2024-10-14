import js
# from pyscript import window, document
import pyodide
from pyodide.ffi import create_proxy
import PIL
from PIL import Image
import io
import json
import base64
import string
import random

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

    for file_id, f in enumerate(file_input.files):
        print(f.name)

        # FileReaderを使用してファイルを読み込む
        reader = js.FileReader.new()
        reader.readAsArrayBuffer(f)

        def on_load(event: pyodide.ffi.JsProxy):
            """
            変換処理のボタンが押された時の処理
            """
            buffer = event.target.result
            image_byte = buffer.to_bytes()
            image = Image.open(io.BytesIO(image_byte))
            print(f"image size {image.size}")
            # print(f"file name : {event.target.name}")

            # _file = buffer.to_file()
            # print(_file)
            # print(dir(_file))

            # 画像処理
            new_image = padding(image, (0, 0, 0), aspect, upper_rate)

            # 画像をbase64エンコードされた文字列に変換
            buffered = io.BytesIO()
            new_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            # 出力画像を表示
            output_image = js.document.getElementById(f'outputImage')
            output_image.src = f"data:image/png;base64,{img_str}"

            # Create and append img element
            img_elem = js.Image.new()
            img_elem.src = f"data:image/png;base64,{img_str}"
            img_elem.width = "200"
            js.document.getElementById("imageContainer").appendChild(img_elem)

            # ダウンロード用の要素を作成
            # ダウンロード用の要素を作成
            download_button = js.document.createElement('button')
            download_button.textContent = f"ダウンロード"
            download_button.style.display = 'block'
            download_button.style.marginTop = '10px'
            download_button.onclick = create_proxy(lambda event: download_image(img_str, f.name))
            
            # ダウンロードリンクを画像コンテナに追加
            js.document.getElementById("imageContainer").appendChild(download_button)

        reader.onload = create_proxy(on_load)

def download_image(img_str: str, filename: str):
    """
    画像をダウンロードする関数

    Note:
        ファイル名は、適当な文字列にする
    """
    download_link = js.document.createElement('a')
    download_link.href = f"data:image/png;base64,{img_str}"
    chars = string.ascii_letters + string.digits
    file_name = ''.join([random.choice(chars) for i in range(5)])
    download_link.download = f"processed_{file_name}.jpg"
    download_link.click()

def padding(pil_img: PIL.Image.Image, 
            background_color: tuple[int], 
            aspect: float, 
            upper_rate: int):
    """
    枠を埋める処理

    Args:
        pil_img (PIL.Image.Image): 処理する元の画像。
        background_color (tuple): 枠の背景色。(R, G, B)形式。
        aspect (float): 目標のアスペクト比（高さ/幅）。
        upper_rate (int): 上部の余白の割合（1-9の範囲）。

    Returns:
        PIL.Image.Image: 枠が追加された新しい画像。

    Note:
        - 元の画像が目標のアスペクト比より横長の場合、上下に枠を追加。
        - 元の画像が目標のアスペクト比より縦長の場合、左右に枠を追加。
        - upper_rateは上下に枠を追加する場合のみ使用され、上部の余白の割合を決定。
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