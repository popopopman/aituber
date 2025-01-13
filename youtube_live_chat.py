import os
import time
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class YouTubeLiveChat:
    def __init__(self, api_key):
        """
        YouTubeライブチャットからコメントを取得するクラス
        :param api_key: YouTube APIキー
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_live_chat_id(self, video_id):
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

    def fetch_live_chat_messages(self, live_chat_id, page_token=None):
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


def main():
    # .env からAPIキーをロード
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise EnvironmentError("Google APIキーが設定されていません。環境変数 'YOUTUBE_API_KEY' を設定してください。")

    # YouTubeのライブ配信のビデオIDを指定
    video_id = input("YouTubeライブ配信のビデオIDを入力してください: ")

    # YouTubeLiveChatインスタンスを作成
    yt_chat = YouTubeLiveChat(api_key)

    try:
        live_chat_id = yt_chat.get_live_chat_id(video_id)
        logger.info(f"ライブチャットID: {live_chat_id}")
    except Exception as e:
        logger.error(f"ライブチャットIDの取得に失敗しました: {e}")
        return

    next_page_token = None
    while True:
        try:
            messages, next_page_token = yt_chat.fetch_live_chat_messages(live_chat_id, next_page_token)

            for message in messages:
                author = message["authorDetails"]["displayName"]
                text = message["snippet"]["displayMessage"]
                logger.info(f"{author}: {text}")

            # レート制限を防ぐために5秒待機
            time.sleep(5)
        except Exception as e:
            logger.error(f"チャットメッセージの取得中にエラーが発生しました: {e}")
            break


if __name__ == "__main__":
    main()
