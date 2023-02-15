# 概要
レアゾン・ヒューマンインタラクション研究所が開発した高精度な音声認識モデル、Reazon SpeechのDockerfileを格納したプロジェクト

# 使い方
1. このプロジェクトをインストール

2. `reazon_speech/`で以下のコマンドを実行してdocker をビルド
```
docker compose build
```

3. 以下のコマンドでコンテナを起動してコンテナに入る
```
docker compose up -d
docker compose exec -it core bash
```

3. 以下のコマンドで仮想環境を起動
```
. activate_python.sh
```

4. 以下のコマンドで`/src`に移動
```
cd /src
```

5. 以下のコマンドでモデルに音声を認識させる。この時音声ファイルは自分で用意する。例に挙げている音声ファイルは公式が公開しているこのファイル（https://research.reazon.jp/_downloads/a8f2c35bb3d351a76212b2257d5bfc85/speech-001.wav）
```
 python3 decode.py  speech-001.wav
```

6. 以下のような認識結果が表示されれば成功
```
気象庁は雪や路面の凍結による交通への影響暴風雪や高波に警戒するとともに雪崩や屋根からの落雪にも十分注意するよう呼びかけています
```