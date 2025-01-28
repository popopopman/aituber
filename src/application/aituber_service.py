import logging
from domain.services.ai_response_service import AIResponseService
from domain.services.text_to_speech_service import TextToSpeechService
from application.youtube_live_service import YouTubeLiveService

logger = logging.getLogger(__name__)

class AITuberService:
    def __init__(self):
        self.youtube_live_service = YouTubeLiveService()
        self.ai_response_service = AIResponseService()
        self.text_to_speech_service = TextToSpeechService()

    def start(self, video_id):
        live_chat_id = self.youtube_live_service.get_live_chat_id(video_id)
        logger.info(f"ライブチャットID: {live_chat_id}")

        while True:
            messages = self.youtube_live_service.fetch_messages(live_chat_id)
            if messages:
                for message in messages:
                    response = self.ai_response_service.generate_response(message.content)
                    self.text_to_speech_service.synthesize_and_play(response.content)
