#!/bin/bash
set -xe

cmd="pip install \
    moviepy yt-dlp \
    ffmpeg-python \
    openai \
    nvidia_smi"

if `python -c "import whisperx"` ; then
    echo "whisperx is already installed, check if it can be upgraded"
    pip install git+https://github.com/m-bain/whisperx.git --upgrade
else
    echo "first time install"
    cmd="$cmd git+https://github.com/m-bain/whisperx.git"
    $cmd
fi
