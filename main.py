from aituber import Aituber


def main():
    video_id = input("YouTubeライブ配信のビデオIDを入力してください: ")
    aituber = Aituber(video_id)
    aituber.handler()


if __name__ == "__main__":
    main()
