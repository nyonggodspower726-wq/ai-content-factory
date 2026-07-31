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
    CompositeAudioClip,
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
                        and file.get("width", 0) >= 1080
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

            clip = VideoFileClip(filename)
            clip.get_frame(0)
            clip.close()

            downloaded.append(filename)

            print(f"Downloaded valid clip {i+1}")

        except Exception as e:

            print(f"Removing corrupted clip: {filename}")
            print(e)

            if os.path.exists(filename):
                os.remove(filename)

    return downloaded


# ==========================================
# BACKGROUND MUSIC
# ==========================================

def add_background_music(video, music_file):

    if not os.path.exists(music_file):

        print("No background music found.")

        return video

    try:

        voice = video.audio

        music = AudioFileClip(
            music_file
        )

        music = music.volumex(0.12)

        music = music.set_duration(
            video.duration
        )

        final_audio = CompositeAudioClip(
            [
                music,
                voice
            ]
        )

        video = video.set_audio(
            final_audio
        )

        print("Background music added.")

        return video

    except Exception as e:

        print(f"Background music failed: {e}")

        return video
# ==========================================
# BUILD BACKGROUND VIDEO
# ==========================================

def build_background_video(video_paths, duration):

    clips = []

    if len(video_paths) == 0:
        return None

    seconds_per_clip = max(
        2,
        duration / len(video_paths)
    )

    for path in video_paths:

        try:

            clip = VideoFileClip(path)

            # Convert to vertical Full HD
            clip = clip.resize(height=1920)

            clip = clip.crop(
                x_center=clip.w / 2,
                y_center=clip.h / 2,
                width=1080,
                height=1920
            )

            clip = clip.subclip(
                0,
                min(
                    seconds_per_clip,
                    clip.duration
                )
            )

            clips.append(clip)

        except Exception as e:

            print(
                f"Failed to load clip {path}: {e}"
            )

    if len(clips) == 0:

        return None

    final_background = concatenate_videoclips(
        clips,
        method="compose"
    )

    final_background = final_background.set_duration(
        duration
    )

    return final_background


# ==========================================
# CREATE FINAL VIDEO
# ==========================================

def create_video(script, voice_file):

    print("Creating professional AI video...")

    keywords = [
        word
        for word in script.split()
        if len(word) > 4
    ]

    search_term = " ".join(
        keywords[:4]
    )

    video_urls = search_pexels_videos(
        search_term
    )

    if len(video_urls) == 0:

        print("No background videos found.")

        return None

    video_paths = download_videos(
        video_urls
    )

    if len(video_paths) == 0:

        print("No valid videos downloaded.")

        return None

    audio = None
    background = None
    final = None
