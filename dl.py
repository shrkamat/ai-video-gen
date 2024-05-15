import yt_dlp
import os
from os import path
from urllib.parse import urlparse, parse_qs


def download_video(session):

    url = session['url']

    parsed_url = urlparse(url)

    if parsed_url.netloc != "www.youtube.com":
        raise Exception("Not a youtube link")
        return

    query_params = parse_qs(parsed_url.query)

    if 'v' not in query_params:
        print("No video id found")
        return

    video_id = query_params['v'][0]

    session['id'] = video_id
    session['dir'] = "dl/{:s}".format(video_id)
    session['video_path'] = "dl/{:s}/output.mp4".format(video_id)

    if path.exists("dl/{:s}/output.mp4".format(video_id)):
        print("Video already downloaded")
        return

    os.makedirs("dl/{:s}".format(video_id), exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': 'dl/{:s}/output.mp4'.format(video_id)
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return video_id

