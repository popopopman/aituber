import os
import time
import logging
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv
from voicevox_synthesizer import VoicevoxSynthesizer
from bedrock_client import BedrockClient
from youtube_live_chat import YouTubeLiveChat
from obs_text_display import OBSTextDisplay

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class Aituber:
    """
    YouTubeライブチャットのメッセージをリアルタイムで処理し、AI応答を生成して音声合成するクラス

    このクラスは、YouTubeライブ配信からチャットメッセージを取得し、AWS Bedrockを使用してAIモデルで応答を生成
    さらに、Voicevoxを使用して応答を音声合成し、リアルタイムで再生
    """

    def __init__(self, video_id):
        """
        環境変数から必要な設定値を読み込み、YouTubeライブチャットおよびAWS Bedrockクライアントを呼ぶ
        引数:
            video_id (str): ライブ配信のYouTubeビデオID

        例外:
            EnvironmentError: 必要な環境変数（AWS認証情報またはYouTube APIキー）が不足している場合に発生
        """
        # 1) .env ファイルからAWS認証情報を読み込む
        load_dotenv()
        # AWSアクセスキーID
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        # AWSシークレットアクセスキー
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        # AWSリージョン
        self.aws_region = os.getenv("AWS_REGION", "ap-northeast-1")
        # Claudeの推論プロファイルARN
        self.inference_profile_arn = os.getenv("MODEL_ARN")
        # YOUTUBEのAPIキー
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        # YouTubeのライブ配信のビデオIDを指定
        self.video_id = video_id
        # YouTubeLiveChatインスタンスを作成
        self.yt_chat = YouTubeLiveChat(self.youtube_api_key)
        self.live_chat_id = self.yt_chat.get_live_chat_id(video_id)
        logger.info(f"ライブチャットID: {self.live_chat_id}")
        # Bedrockクライアントを初期化
        self.bedrock_client = BedrockClient(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.aws_region,
        )
        self.system_prompt = self.read_system_prompt()

    def read_system_prompt(self, file_path="system_prompt.txt"):
        """
        system_prompt.txt からシステムプロンプトを読み込む
        :param file_path: システムプロンプトが記載されたファイルパス
        :return: システムプロンプト文字列
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except FileNotFoundError:
            raise RuntimeError(f"システムプロンプトファイル '{file_path}' が見つかりません。")
        except Exception as e:
            raise RuntimeError(f"システムプロンプトの読み込み中にエラーが発生しました: {e}")

    def handler(self):
        """
        YouTubeライブチャットからメッセージを取得し、AI応答を生成して音声合成を行う

        ライブチャットのメッセージを定期的にポーリングし、以下を実行:
        1. メッセージ取得
        2. AWS Bedrockを使用したAI応答生成
        3. Voicevoxでの音声合成
        4. 合成音声の再生

        例外が発生した場合、ロガーを使用してエラーを記録し、処理を終了

        例外:
            Exception: ライブチャットの取得または音声合成中にエラーが発生した場合
        """
        try:
            next_page_token = None
            while True:
                try:
                    # メッセージ取得
                    messages, next_page_token = self.yt_chat.fetch_live_chat_messages(
                        self.live_chat_id, next_page_token
                    )

                    for message in messages:
                        author = message.get("authorDetails", {}).get("displayName", "不明なユーザー")
                        snippet = message.get("snippet", {})
                        text = snippet.get("displayMessage", "メッセージがありません")

                        logger.info(f"{author}: {text}")

                        # メッセージが空の場合はスキップ
                        if text == "メッセージがありません":
                            logger.warning("無効なメッセージをスキップしました")
                            continue

                    # 取得したメッセージの1番目をBedrockに問い合わせ
                    if not messages:
                        logger.warning("メッセージが取得できませんでした。スキップします。")
                        return

                    # 最初のメッセージを取得
                    first_message = messages[0]
                    snippet = first_message.get("snippet", {})
                    request_message = snippet.get("displayMessage")

                    if not request_message:
                        logger.warning("最初のメッセージが無効です。スキップします。")
                        return

                    prompt = f"{self.system_prompt} {request_message}"

                    # AWS Bedrockを使用したAI応答生成
                    response_text = self.bedrock_client.query_claude_with_profile(
                        inference_profile_arn=self.inference_profile_arn, prompt=prompt
                    )[0]["text"]

                    logger.info("=== Claudeの応答 ===")
                    logger.info(f"response_text: {response_text}")

                    # Voicevoxで音声合成
                    voicevox = VoicevoxSynthesizer()
                    output_wav = "bedrock_response.wav"
                    voicevox.synthesize(text=response_text, speaker_id=47, filename=output_wav)

                    # 合成音声の再生
                    if os.path.exists(output_wav):
                        data, samplerate = sf.read(output_wav)
                        sd.play(data, samplerate)
                        sd.wait()  # 再生が終了するまで待機
                        logger.info("再生が完了しました")
                    else:
                        logger.error(f"エラー: ファイル '{output_wav}' が存在しません", exc_info=True)

                    # レート制限を防ぐために10秒待機
                    time.sleep(10)
                except Exception as e:
                    logger.error(f"チャットメッセージの取得中にエラーが発生しました: {e}")
                    break

            if not self.aws_access_key or not self.aws_secret_key:
                raise EnvironmentError("AWS_ACCESS_KEY_ID または AWS_SECRET_ACCESS_KEY が見つかりません")

        except Exception as e:
            logger.error(f"エラーが発生しました: {e}", exc_info=True)
