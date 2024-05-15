from dl import download_video
from ffmpeg_util import extract_audio


def start():
    print("Hello World!")
    session = {}
    try:
        session['url'] = "https://www.youtube.com/watch?v=N9zpRvFRmj8"
        download_video(session)
        extract_audio(session)
    except Exception as e:
        print("Failure: ", e)
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    start()
