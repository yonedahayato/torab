# ffmpge (ffplay) を使って、カメラの画像を出力
# https://diysmartmatter.com/archives/349

ffplay -pixel_format uyvy422 -framerate 30 -f avfoundation -i "GENERAL WEBCAM"
