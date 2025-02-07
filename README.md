# AITuber

YouTube ライブチャットからメッセージを取得し、AI応答を生成、音声合成を行うシステムです。

---

## 環境構築

### **1. Poetry のインストール**

Poetry がインストールされていない場合は、以下のコマンドでインストールしてください。

``` sh
pip install --upgrade pip
pip install poetry==1.5.1
```

### **2. プロジェクト依存関係のインストール**

プロジェクトルートディレクトリで以下のコマンドを実行します。

``` sh
poetry install
```

### **3. voicevox_engineのpull**

VOICEVOX の音声合成エンジンのイメージをoullします。

``` sh
docker pull voicevox/voicevox_engine:nvidia-latest
```

### **4. .envファイルの作成**

プロジェクトのルートディレクトリに `.env` ファイルを作成し、以下の情報を記述してください。

``` sh
PYTHONPATH=src
AWS_ACCESS_KEY=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
AWS_REGION=ap-northeast-1
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
MODEL_ARN=anthropic.claude-3-haiku-20240307-v1:0
```

- `PYTHONPATH`: Pythonのモジュール検索パス
- `AWS_ACCESS_KEY`: AWSアクセスキー
- `AWS_SECRET_ACCESS_KEY`: AWSシークレットアクセスキー
- `AWS_REGION`: AWSリージョン (例: `ap-northeast-1`)
- `YOUTUBE_API_KEY`: YouTube Data API v3が利用可能なAPIキー
- `MODEL_ARN`: 使用するAIモデルのARN（claudeを想定した実装になっている）

## 実行方法

### **1. VOICEVOX エンジンの起動**

VOICEVOX の音声合成エンジンを起動します。

``` sh
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
```

注意:
--gpus all オプションは GPU を使用する環境でのみ必要です。GPU を使用しない場合はこのオプションを省略してください。

### **2. プロジェクトの実行**
以下のコマンドでスクリプトを実行します。

``` sh
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
