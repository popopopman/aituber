import logging
from application.aituber_service import AITuberService

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class AITuberCLI:
    def __init__(self):
        self.aituber_service = AITuberService()

    def run(self):
        video_id = input("YouTubeライブ配信のビデオIDを入力してください: ")
        self.aituber_service.start(video_id)

def main():
    cli = AITuberCLI()
    cli.run()

if __name__ == "__main__":
    main()