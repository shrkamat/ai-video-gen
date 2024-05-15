from dl import download_video
from ffmpeg_util import extract_audio
from transcribe import transcribe
from ai_openai import extract_highlights


def start():
    print("Hello World!")
    session = {}
    try:
        session['url'] = "https://www.youtube.com/watch?v=N9zpRvFRmj8"
        download_video(session)
        extract_audio(session)
        transcribe(session)
        subs1 = extract_highlights(session['audio_str'])
    except Exception as e:
        print("Failure: ", e)
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    start()
