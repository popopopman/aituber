from infrastructure.youtube_api_client import YouTubeAPIClient
from utils.logger import setup_logger

logger = setup_logger(__name__)

class YouTubeLiveService:
    def __init__(self):
        """
        YouTubeライブチャットからコメントを取得するクラス
        """
        self.api_client = YouTubeAPIClient()

    def get_live_chat_id(self, video_id: str) -> str:
        """
        指定したYouTubeライブ配信のチャットIDを取得
        :param video_id: YouTubeライブ配信のビデオID
        :return: ライブチャットID
        """
        return self.api_client.get_live_chat_id(video_id)

    def fetch_messages(self, live_chat_id: str, page_token: str = None) -> tuple:
        """
        ライブチャットのメッセージを取得
        :param live_chat_id: ライブチャットID
        :param page_token: 次のページのトークン
        :return: チャットメッセージリスト、次のページトークン
        """
        return self.api_client.fetch_messages(live_chat_id, page_token)
