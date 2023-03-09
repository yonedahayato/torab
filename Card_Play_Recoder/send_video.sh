# video を送信する
# https://qiita.com/fukasawah/items/32ebef9cd646a1eb3e3a

ffmpeg -pixel_format uyvy422 -framerate 30 -f avfoundation -i "GENERAL WEBCAM" -f mpegts "tcp://127.0.0.1:12345?listen=1&tcp_nodelay=1"
