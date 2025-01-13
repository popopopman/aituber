import requests
import json
import time
import logging

# ロガーの設定
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class VoicevoxSynthesizer:
    """
    Voicevox エンジンを使ってテキストを音声に変換するクラス
    """

    def __init__(self, base_url="http://127.0.0.1:50021", max_retry=3, retry_interval=1):
        """
        :param base_url: Voicevox エンジンのベースURL
        :param max_retry: APIリクエストの最大リトライ回数
        :param retry_interval: リトライ間隔（秒）
        """
        self.base_url = base_url
        self.max_retry = max_retry
        self.retry_interval = retry_interval

    def audio_query(self, text, speaker_id):
        """
        音声合成用クエリを作成します。
        :param text: 合成するテキスト
        :param speaker_id: スピーカーID
        :return: audio_query API のレスポンスデータ
        """
        query_payload = {"text": text, "speaker": speaker_id}
        for attempt in range(self.max_retry):
            try:
                response = requests.post(f"{self.base_url}/audio_query", params=query_payload, timeout=(10.0, 300.0))
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.error(f"audio_query API エラー（試行 {attempt + 1}/{self.max_retry}）: {e}")
                time.sleep(self.retry_interval)
        raise RuntimeError("audio_query API 接続に失敗しました。")

    def synthesis(self, query_data, speaker_id):
        """
        音声を合成します。
        :param query_data: audio_query API で取得したデータ
        :param speaker_id: スピーカーID
        :return: 音声データ (バイナリ)
        """
        synth_payload = {"speaker": speaker_id}
        for attempt in range(self.max_retry):
            try:
                response = requests.post(
                    f"{self.base_url}/synthesis",
                    params=synth_payload,
                    data=json.dumps(query_data),
                    headers={"Content-Type": "application/json"},
                    timeout=(10.0, 300.0),
                )
                logger.info(f"audio_query レスポンス: {response}")
                response.raise_for_status()
                logger.info(f"音声合成: スピーカーID={speaker_id}")
                return response.content
            except requests.exceptions.RequestException as e:
                logger.error(f"synthesis API エラー（試行 {attempt + 1}/{self.max_retry}）: {e}")
                time.sleep(self.retry_interval)
        raise RuntimeError("synthesis API 接続に失敗しました。")

    def synthesize(self, text, speaker_id=47, filename="output.wav"):
        """
        テキストを音声に変換してファイルに保存します。
        :param text: 合成するテキスト
        :param speaker_id: スピーカーID
        :param filename: 保存するファイル名
        """
        logger.info(f"音声合成開始: スピーカーID={speaker_id}")

        # audio_query API を呼び出し
        query_data = self.audio_query(text, speaker_id)
        if not query_data:
            raise RuntimeError("audio_query API のレスポンスが不正です。")

        # synthesis API を呼び出し
        voice_data = self.synthesis(query_data, speaker_id)
        if not voice_data:
            raise RuntimeError("synthesis API のレスポンスが不正です。")

        # 音声データをファイルに保存
        try:
            with open(filename, "wb") as f:
                f.write(voice_data)
            logger.info(f"音声合成完了: ファイル='{filename}'")
        except IOError as e:
            raise RuntimeError(f"音声ファイルの保存中にエラーが発生しました: {e}")


def main():
    import sounddevice as sd
    import soundfile as sf
    import os

    # テスト実行用
    synthesizer = VoicevoxSynthesizer()
    test_text = "これはボイスのテストです。"
    try:
        output_wav = "test_sasayaki.wav"
        voicevox = VoicevoxSynthesizer()
        voicevox.synthesize(text=test_text, speaker_id=47, filename=output_wav)
        if os.path.exists(output_wav):
            data, samplerate = sf.read(output_wav)
            sd.play(data, samplerate)
            sd.wait()  # 再生が終了するまで待機
            logger.info("再生が完了しました")
        else:
            logger.error(f"エラー: ファイル '{output_wav}' が存在しません", exc_info=True)
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
