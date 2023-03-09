# ffmpge (ffplay) を使って、カメラの画像を出力

ffplay -pixel_format uyvy422 -framerate 30 -f avfoundation -i "GENERAL WEBCAM"
