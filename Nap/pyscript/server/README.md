# pyscript の実行環境を再現するための server

pyscript の worker 上で terminal を実行するには、以下の設定が必要だったので、server.py を実装

```
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Resource-Policy: cross-origin
```

だが、github pages は、これらに対応できないため、以下の方法を検討

1. 実装した server.py を利用するために、他のホスティングサービスを探す
1. github pages の範囲で、できる表現を探す (pyscript の worker 上で terminal を使わない)

後者を選択したため、server.py は不要