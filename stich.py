#!/usr/bin/env python
from __future__ import unicode_literals
from moviepy.editor import VideoFileClip, concatenate_videoclips
import json
import os
from pathlib import Path


import imageio

imageio.plugins.ffmpeg.download()


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

    for region in segIds:
        segment = data[region]
        start = segment["start"] - 0.500
        end = segment["end"] + 0.500

        print(str(start)+"-->"+str(end)+": \t"+segment["text"])
        subclip = input_video.subclip(start, end)
        subclips.append(subclip)

    # Closing file
    tokenized_subtitles.close()
    return concatenate_videoclips(subclips)


def create_summary_video(session):
    summary = create_summary(session['video_path'], session['segIds'],
                             session['audio_tok_path'])
    output_path = Path(session['dir']) / "summary.mp4"
    summary.to_videofile(
        output_path,
        codec="libx264",
        temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac")

