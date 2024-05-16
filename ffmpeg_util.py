from pathlib import Path
import ffmpeg


def extract_audio(session):
    video_path = session['video_path']
    audio_path = Path(session['dir']) / "audio.mp3"

    if audio_path.exists():
        print('audio already extracted!')
        session['audio_path'] = str(audio_path)
        return

    # Ensure the video path is a string
    video_path_str = str(video_path)

    # Ensure the audio path is a string
    audio_path_str = str(audio_path)

    print("Extracting audio from video")
    print("Video path: ", video_path_str)
    print("Audio path: ", audio_path_str)

    # Run ffmpeg command
    ffmpeg.input(video_path_str).output(
        audio_path_str, acodec='libmp3lame').run()

    session['audio_path'] = audio_path_str
