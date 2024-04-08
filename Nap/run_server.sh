OPTION=${1}

if [ $OPTION == "pyscript" ]; then
    # pyscript の worker 上で terminal を実行するには、以下の設定が必要だったので、server.py を実装
    #   Cross-Origin-Opener-Policy: same-origin
    #   Cross-Origin-Embedder-Policy: require-corp
    #   Cross-Origin-Resource-Policy: cross-origin
    python3 ./pyscript/server/server.py

else
    python3 -m http.server
fi