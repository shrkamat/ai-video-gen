from pathlib import Path
import ffmpeg


def extract_audio(session):
    video_path = session['video_path']
    audio_dir = Path(session['dir'])
    audio_path = audio_dir / "audio.mp3"

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



