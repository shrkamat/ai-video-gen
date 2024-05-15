import whisperx
import json
import math

(device, compute) = ("cuda", "fp16")
# (device, compute) = ("cpu", "fp32")


def seconds_to_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    (ms, sec) = math.modf(remaining_seconds)
    return '{:02d}:{:02d}:{:02d},{:03d}'.format(
        int(hours), int(minutes), int(sec), int(ms*1000))


def transcribe(audio_file):

    model_x = whisperx.load_model(
        "medium.en", device=device, compute_type=compute)
    audio = whisperx.load_audio(audio_file)

    result = model_x.transcribe(audio, batch_size=16)

    with open("audio_orig.json", "w") as f:
        f.write(json.dumps(result['segments'], indent=4))

    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device)

    result_a = whisperx.align(
        result["segments"], model_a, metadata, audio, device=device,
        return_char_alignments=False)

    with open("audio_tokenized.json", "w") as f:
        f.write(json.dumps(result_a['segments'], indent=4))

    with open("audio.srt", "w") as f:
        for idx, seg in enumerate(result_a['segments']):
            res = ''

            # uncomment below lines to create srt file with timestamps
            # start = seconds_to_timestamp(seg['start'])
            # end = seconds_to_timestamp(seg['end'])
            # res += '\n{:d}\n{:s} --> {:s}\n'.format(
            #     idx, start, end)

            res += '{:s}\n'.format(seg['text'].strip())
            f.write(res)
