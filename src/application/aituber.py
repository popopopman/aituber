import logging
import time
from domain.services.ai_response_servidce import AIResponseService
from domain.services.text_to_speech_service import TextToSpeechService
from domain.services.youtube_live_service import YouTubeLiveService

logger = logging.getLogger(__name__)

class AITuber:
    def __init__(self):
        """
        AITuber クラスのコンストラクタ。
        YouTube ライブチャットからコメントを取得し、AI で応答を生成し、音声合成して再生するサービスを提供する。
        """
        self.youtube_live_service = YouTubeLiveService()
        self.ai_response_service = AIResponseService()
        self.text_to_speech_service = TextToSpeechService()

    def start(self, video_id: str) -> None:
        """
        指定された YouTube ライブ配信のビデオ ID を使用してサービスを開始する。
        
        :param video_id: YouTube ライブ配信のビデオ ID
        """
        # ライブチャット ID を取得
        live_chat_id = self.youtube_live_service.get_live_chat_id(video_id)
        logger.info(f"ライブチャットID: {live_chat_id}")
        system_prompt_file = 'src/config/system_prompt.txt'
        system_prompt = self.ai_response_service.load_system_prompt(system_prompt_file)
        while True:
            # ライブチャットのメッセージを取得
            messages, _ = self.youtube_live_service.fetch_messages(live_chat_id)
            if messages:
                for message in messages:
                    # メッセージから応答を生成
                    response = self.ai_response_service.generate_response(message['snippet']['displayMessage'], system_prompt)
                    # 応答を音声合成して再生
                    self.text_to_speech_service.synthesize_and_play(response.content)
            # YouTube API のクオータ上限を超えないように、10 秒間スリープしてリクエスト間隔を調整
            time.sleep(10)
