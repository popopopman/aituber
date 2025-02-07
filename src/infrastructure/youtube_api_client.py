from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

class YouTubeAPIClient:
    def __init__(self):
        """
        YouTube API クライアント
        """
        self.api_key = YOUTUBE_API_KEY
        if not self.api_key:
            raise EnvironmentError("Google APIキーが設定されていません。環境変数 'YOUTUBE_API_KEY' を設定してください。")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_live_chat_id(self, video_id: str) -> str:
        """
        指定したYouTubeライブ配信のチャットIDを取得
        :param video_id: YouTubeライブ配信のビデオID
        :return: ライブチャットID
        """
        response = self.youtube.videos().list(part="liveStreamingDetails", id=video_id).execute()
        if not response["items"]:
            raise ValueError("指定されたビデオIDが無効か、ライブ配信が存在しません。")
        live_chat_id = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
        return live_chat_id

    def fetch_messages(self, live_chat_id: str, page_token: str = None) -> tuple:
        """
        ライブチャットのメッセージを取得
        :param live_chat_id: ライブチャットID
        :param page_token: 次のページのトークン
        :return: チャットメッセージリスト、次のページトークン
        """
        response = (
            self.youtube.liveChatMessages()
            .list(
                liveChatId=live_chat_id,
                part="snippet,authorDetails",
                pageToken=page_token,
                maxResults=200,
            )
            .execute()
        )
        messages = response.get("items", [])
        next_page_token = response.get("nextPageToken")
        return messages, next_page_token
