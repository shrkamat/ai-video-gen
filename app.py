import sys
import traceback

from dl import download_video
from ffmpeg_util import extract_audio
from transcribe import transcribe
from ai_openai import extract_highlights
from stich import create_summary_video


def start(url):
    print("Hello World!")
    session = {}
    try:
        session['url'] = url
        download_video(session)
        extract_audio(session)
        transcribe(session)
        extract_highlights(session)
        create_summary_video(session)
    except Exception as e:
        print("Failure: ", e)
        print(traceback.format_exc())
    finally:
        print("Goodbye!")


if __name__ == "__main__":
    arg = sys.argv[1]
    start(arg)
