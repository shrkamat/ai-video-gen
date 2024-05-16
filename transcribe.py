import whisperx
import json
import math
from pathlib import Path

(device, compute) = ("cuda", "float16")
# (device, compute) = ("cpu", "float32")


def seconds_to_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    (ms, sec) = math.modf(remaining_seconds)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(
        int(hours), int(minutes), int(sec), int(ms*1000))


def write_json_file(session, data, filename):
    file_path = Path(session['dir']) / filename
    with open(str(file_path), 'w') as f:
        f.write(json.dumps(data, indent=4))
    return file_path


def write_file(session, data, filename):
    file_path = Path(session['dir']) / filename
    with open(str(file_path), 'w') as f:
        f.write(data)
    return file_path


def transcribe(session):

    audio_file = session['audio_path']

    audio_srt_path = Path(session['dir']) / 'audio.srt'

    if audio_srt_path.exists():
        print('transcribe already complete!')

        session['audio_srt_path'] = str(audio_srt_path)
        session['audio_tok_path'] = str(Path(session['dir']) / 'audio_tokenized.json')
        return

    # transcribe stage 1
    model_x = whisperx.load_model(
        "medium.en", device=device, compute_type=compute)
    audio = whisperx.load_audio(audio_file)

    result = model_x.transcribe(audio, batch_size=16)

    write_json_file(session, result['segments'], 'audio_orig.json')

    # transcribe stage 2
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device)

    result_a = whisperx.align(
        result['segments'], model_a, metadata, audio, device=device,
        return_char_alignments=False)

    session['audio_tok_path'] = write_json_file(
        session, result_a['segments'], 'audio_tokenized.json')

    res = ''
    for idx, seg in enumerate(result_a['segments']):
        # uncomment below lines to create srt file with timestamps
        # start = seconds_to_timestamp(seg['start'])
        # end = seconds_to_timestamp(seg['end'])
        # res += '\n{:d}\n{:s} --> {:s}\n'.format(
        #     idx, start, end)

        res += '{:s}\n'.format(seg['text'].strip())

    session['audio_srt_path'] = write_file(session, res, 'audio.srt')
