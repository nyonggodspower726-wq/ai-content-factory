import os
import requests
import PIL.Image

# Pillow compatibility
if not hasattr(PIL.Image, "ANTIALIAS"):
    try:
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS


from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips,
)

from config import PEXELS_API_KEY
from video.effects import add_hook
from video.subtitles import add_subtitles


# ==========================================
# SEARCH PEXELS VIDEOS
# ==========================================

def search_pexels_videos(query):

    print(f"Searching Pexels: {query}")

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

        response.raise_for_status()

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


# ==========================================
# DOWNLOAD VIDEOS
# ==========================================

def download_videos(video_urls):

    os.makedirs("output/clips", exist_ok=True)

    downloaded = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, url in enumerate(video_urls):

        filename = f"output/clips/clip_{i}.mp4"

        try:

            response = requests.get(
                url,
                headers=headers,
                stream=True,
                timeout=60
            )

            response.raise_for_status()

            print("Downloading video...")

            with open(filename, "wb") as f:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:
                        f.write(chunk)

            test_clip = VideoFileClip(filename)
            test_clip.close()

            downloaded.append(filename)

            print(f"Downloaded clip {i + 1}")

        except Exception as e:

            print(f"Skipping corrupted video: {filename}")
            print(e)

    return downloaded
