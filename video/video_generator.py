import os
import requests
import subprocess
import PIL.Image

# Fix MoviePy + Pillow compatibility
if not hasattr(PIL.Image, "ANTIALIAS"):
    try:
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips
)

from config import PEXELS_API_KEY
from video.subtitle_generator import create_subtitles
from video.effects import add_hook


# ============================================
# SEARCH MULTIPLE PEXELS VIDEOS
# ============================================

def search_pexels_videos(query):

    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 5
    }

    videos = []

    try:

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        data = response.json()

        if "videos" in data:

            for video in data["videos"]:

                for file in video["video_files"]:

                    if (
                        file.get("link", "").endswith(".mp4")
                        and file.get("width", 0) >= 720
                    ):

                        videos.append(file["link"])
                        break

    except Exception as e:

        print(f"Pexels search failed: {e}")

    return videos


# ============================================
# DOWNLOAD MULTIPLE VIDEOS
# ============================================

def download_videos(video_urls):

    os.makedirs("output/clips", exist_ok=True)

    clips = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for index, url in enumerate(video_urls):

        path = f"output/clips/clip_{index}.mp4"

        response = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        with open(path, "wb") as f:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    f.write(chunk)

        print(f"Downloaded clip {index + 1}")

        clips.append(path)

    return clips
# ============================================
# BUILD PROFESSIONAL BACKGROUND VIDEO
# ============================================

def build_background_video(video_paths, duration):

    clips = []

    if len(video_paths) == 0:
        return None

    seconds_per_clip = max(
        2,
        duration / len(video_paths)
    )

    for path in video_paths:

        clip = VideoFileClip(path)

        clip = clip.resize(
            height=1280
        )

        clip = clip.crop(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=720,
            height=1280
        )

        clip = clip.subclip(
            0,
            min(
                seconds_per_clip,
                clip.duration
            )
        )

        clips.append(clip)

    final_background = concatenate_videoclips(
        clips,
        method="compose"
    )

    final_background = final_background.set_duration(
        duration
    )

    return final_background


# ============================================
# BURN SUBTITLES
# ============================================

def burn_subtitles(video_file, subtitle_file):

    print("Burning captions into video...")

    output = "output/final_caption_video.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
        "-vf",
        f"subtitles={subtitle_file}",
        "-c:v",
        "libx264",
        "-c:a",
        "copy",
        output
    ]

    try:

        subprocess.run(
            command,
            check=True
        )

        print("Captions burned successfully.")

        return output

    except Exception as e:

        print(f"Caption burn failed: {e}")

        return video_file
