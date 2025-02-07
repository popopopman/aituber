import os
from dotenv import load_dotenv

# .env ファイルを読み込む
load_dotenv()

# 環境変数を取得
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-1")
MODEL_ARN = os.getenv("MODEL_ARN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
