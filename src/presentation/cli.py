import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger
from application.aituber import AITuber

logger = setup_logger(__name__)

class AITuberCLI:
    def __init__(self):
        self.aituber = AITuber()

    def run(self):
        video_id = input("YouTubeライブ配信のビデオIDを入力してください: ")
        self.aituber.start(video_id)

def main():
    cli = AITuberCLI()
    cli.run()

if __name__ == "__main__":
    main()