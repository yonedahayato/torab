import js
from pyscript import window, document
from pyodide.ffi import create_proxy
from PIL import Image
import io
import base64

def resize_image(event):
    """
    """
    # 入力画像の取得
    print("resize image")
    # file_input = document.getElementById('imageInput')
    file_input = js.document.querySelector('#imageInput')

    file = file_input.value
    
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
    # reader.readAsArrayBuffer(file)
    # reader.readAsDataURL(file)
    print([f for f in file_input.files])

    for f in file_input.files:
        reader.readAsArrayBuffer(f)
        break
    
    def on_load(event):
        buffer = event.target.result
        image_byte = buffer.to_bytes()
        image = Image.open(io.BytesIO(image_byte))
        print(f"image size {image.size}")
        width, height = image.size
        
        # 画像のリサイズ
        new_image = image.resize((new_width, new_height))
        new_image = expand2square(image, (0, 0, 0))

        # 画像をbase64エンコードされた文字列に変換
        buffered = io.BytesIO()
        new_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # 出力画像を表示
        output_image = js.document.getElementById('outputImage')
        output_image.src = f"data:image/png;base64,{img_str}"
    
    reader.onload = create_proxy(on_load)

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result