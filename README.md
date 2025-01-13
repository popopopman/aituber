# aituberを作ろう

# コマンド
## 環境構築
python -m venv .aituber
.aituber\Scripts\activate

pip install --upgrade pip
pip install poetry==1.5.1
poetry lock
poetry install

docker pull voicevox/voicevox_engine:nvidia-latest

## 実行
.aituber\Scripts\activate
docker run --rm --gpus all -p '127.0.0.1:50021:50021' voicevox/voicevox_engine:nvidia-latest
python main.py

