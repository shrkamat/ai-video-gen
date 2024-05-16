#!/usr/bin/env python
from __future__ import unicode_literals
from moviepy.editor import VideoFileClip, CompositeVideoClip
import json
from pathlib import Path

import imageio


if imageio.plugins.ffmpeg.get_exe() is None:
    imageio.plugins.ffmpeg.download()


def create_summary(video_file, segIds, audio_tok_file):
    """ Join segments

    Args:
        filename(str): filename
        regions():
    Returns:
        VideoFileClip: joined subclips in segment

    """

    # Opening JSON file
    tokenized_subtitles = open(audio_tok_file, 'r')

    # returns JSON object as
    # a dictionary
    data = json.load(tokenized_subtitles)

    subclips = []
    input_video = VideoFileClip(video_file)
    black_video = VideoFileClip("blackVideo.mp4")
    black_video_clip = black_video.subclip(0, 1)
    black_video_clip.set_fps(60)
    counter = 0
    continuation = False
    start = 0
    total_regions = len(segIds)
    print(str(total_regions))
    for setId in segIds:
        last_region = segIds[-1] == setId
        segment = data[setId]
        end_this = segment["end"]
        start_next = 0

        further_continuation = False
        if not last_region:
            # print(data[(regions[counter+1])])
            start_next = data[(segIds[counter+1])]["start"]
            # further_continuation = regions[counter] == (regions[counter+1]-1)
            print("start_next="+str(start_next)+",end_this="+str(end_this))
            further_continuation = start_next - end_this < 1.0
        else:
            further_continuation = False

        print("i="+str(counter)+":"+str(setId)+",last_region="+str(last_region),
              "further_continuation="+str(further_continuation)+",continuation="+str(continuation))

        if last_region:
            if continuation:
                print("cond:1.1")
                end = segment["end"]
                print(str(start)+"-->"+str(end)+": \t"+segment["text"])
                subclip = input_video.subclip(start, end)
                subclips.append(subclip)
            else:
                print("cond:1.2")
                start = segment["start"] - 0.500
                end = segment["end"]
                print(str(start)+"-->"+str(end)+": \t"+segment["text"])
                subclip = input_video.subclip(start, end)
                subclips.append(subclip)
            continuation = False
        elif continuation:
            if further_continuation:
                print("cond:2.1 = this is middle clip no operation will be merged fully")
            else:
                print("cond:2.2 = no further continuation clip")
                end = segment["end"]
                subclip = input_video.subclip(start, end)
                print(str(start)+"-->"+str(end)+": \t"+segment["text"])
                subclips.append(subclip)
                continuation = False
        elif further_continuation:
            print("cond:3 new continuation found")
            start = segment["start"] - 0.500
            continuation = True
        else:
            print("cond:4 no continuation")
            start = segment["start"] - 0.500
            end = segment["end"] + 0.500
            print(str(start)+"-->"+str(end)+": \t"+segment["text"])
            subclip = input_video.subclip(start, end)
            subclips.append(subclip)
            continuation = False

        # start = segment["start"]- 0.500
        # end = segment["end"] + 0.500
        # subclip = input_video.subclip(segment["start"], segment["end"])

        counter += 1

    fade_time = 0.5
    video_clips = subclips
    video_fx_list = [video_clips[0]]

    idx = video_clips[0].duration - fade_time
    for video in video_clips[1:]:
        print("idx="+str(idx))
        video_fx_list.append(black_video_clip.set_start(
            idx).crossfadein(fade_time))
        idx += black_video_clip.duration - fade_time
        video_fx_list.append(video.set_start(idx).crossfadein(fade_time))
        idx += video.duration - fade_time

    # Closing file
    tokenized_subtitles.close()
    # return concatenate_videoclips(subclips)
    return CompositeVideoClip(video_fx_list)


def create_summary_video(session):
    summary = create_summary(session['video_path'], session['segIds'],
                             session['audio_tok_path'])
    output_path = Path(session['dir']) / "summary.mp4"
    summary.to_videofile(
        output_path,
        codec="libx264",
        temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac", fps=60)


if __name__ == "__main__":
    with open('dl/g_1oiJqE3OI/segIds.json') as f:
        segIds = json.load(f)
        print(type(segIds))
        session = {
            "video_path": "dl/g_1oiJqE3OI/output.mp4",
            "segIds": segIds,
            "audio_tok_path": "dl/g_1oiJqE3OI/audio_tokenized.json",
            "dir": "dl/g_1oiJqE3OI"
        }
        create_summary_video(session)
