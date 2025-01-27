# AITuber

AITuber は、YouTube ライブチャットからメッセージを取得し、AI応答を生成、音声合成を行うプロジェクトです。

---

## 環境構築

### **1. Poetry のインストール**
Poetry がインストールされていない場合は、以下のコマンドでインストールしてください。

``` bash
pip install --upgrade pip
pip install poetry==1.5.1
```

### **2. プロジェクト依存関係のインストール**
プロジェクトルートディレクトリで以下のコマンドを実行します。

- 通常の依存関係のみインストールする場合:

``` bash
poetry install
```

- 開発用依存関係も含めてインストールする場合:

``` bash
poetry install --with dev
```

## 実行方法
### **1. VOICEVOX エンジンの起動**
VOICEVOX の音声合成エンジンを Docker を使用して起動します。

``` bash
docker pull voicevox/voicevox_engine:nvidia-latest
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
```

注意:
--gpus all オプションは GPU を使用する環境でのみ必要です。GPU を使用しない場合はこのオプションを省略してください。

### **2. プロジェクトの実行**
以下のコマンドでスクリプトを実行します。

``` bash
poetry run python src/app/main.py
```

## テスト

### **1. テストの実行**

以下のコマンドでテストを実行します。

``` bash
poetry run pytest
```

### **2. テストカバレッジの測定**

カバレッジを測定するには以下のコマンドを使用します。

``` bash
poetry run pytest --cov=src
```

## その他のコマンド

### 依存関係のロック

依存関係を更新した場合、poetry.lock を生成または更新します。

``` bash
poetry lock
```

``` plaintext
ディレクトリ構成
plaintextaituber/
├── src/
│   ├── app/                # アプリケーションのエントリーポイント
│   │   └── main.py
│   ├── domain/             # ドメインロジック
│   ├── infrastructure/     # 外部サービスとの連携
│   ├── presentation/       # CLI や API を通じた入出力
│   └── tests/              # テストコード
├── pyproject.toml          # Poetry 設定ファイル
└── poetry.lock             # 依存関係のロックファイル
```

## 注意事項

VOICEVOX エンジンを起動するには、Docker がインストールされている必要があります。
