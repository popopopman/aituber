import obswebsocket
from obswebsocket import obsws, requests


class OBSTextDisplay:
    def __init__(self, host="localhost", port=4455, password=""):
        """
        OBS WebSocketに接続します。
        :param host: OBS WebSocketのホスト
        :param port: OBS WebSocketのポート
        :param password: OBS WebSocketのパスワード
        """
        self.ws = obsws(host, port, password)
        self.ws.connect()

    def set_text(self, source_name, text):
        """
        OBSのテキストソースにテキストを設定します。
        :param source_name: テキストソースの名前
        :param text: 表示するテキスト
        """
        try:
            self.ws.call(requests.SetTextGDIPlusProperties(source=source_name, text=text))
            print(f"OBSにテキストを設定しました: {text}")
        except Exception as e:
            print(f"OBSでエラーが発生しました: {e}")

    def disconnect(self):
        """
        OBS WebSocketから切断します。
        """
        self.ws.disconnect()


def main():
    obs = OBSTextDisplay(host="localhost", port=4455, password="VpqbioEeQF39EfQG")
    obs.set_text(source_name="test", text="Hello, OBS!")
    obs.disconnect()


if __name__ == "__main__":
    main()
