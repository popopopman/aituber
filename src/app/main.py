import sys
import os
from dotenv import load_dotenv

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# .env ファイルを読み込む
load_dotenv()

from presentation.cli import main

if __name__ == "__main__":
    main()
