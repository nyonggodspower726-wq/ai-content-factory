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
from video.transitions import apply_zoom
from video.background_music import add_background_music

# ==========================================
# SEARCH MULTIPLE PEXELS VIDEOS
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
# DOWNLOAD MULTIPLE CLIPS
# ==========================================

def download_videos(video_urls):

    os.makedirs("output/clips", exist_ok=True)

    downloaded = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for i, url in enumerate(video_urls):

        filename = f"output/clips/clip_{i}.mp4"

        response = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        with open(filename, "wb") as f:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    f.write(chunk)

        print(f"Downloaded clip {i + 1}")

        downloaded.append(filename)

    return downloaded
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
except Exception:
    print(f"Skipping bad video: {path}")
    continue

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
            min(seconds_per_clip, clip.duration)
        )


        clips.append(clip)


    final_background = concatenate_videoclips(
        clips,
        method="compose"
    )
    final_background = apply_zoom(final_background)

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


    try:

        audio = AudioFileClip(
            voice_file
        )


        background = build_background_video(
            video_paths,
            audio.duration
        )


        if background is None:

            print("Background creation failed.")

            return None


        final = background.set_audio(
            audio
    )
        # ==========================================
        # EXPORT VIDEO
        # ==========================================

        output = "output/final_video.mp4"


        final.write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="ultrafast",
            threads=1,
            logger="bar"
        )


        print("Professional video created.")


        # ==========================================
        # ADD HOOK
        # ==========================================

        hook_text = script.split(".")[0]


        try:

            hooked_video = add_hook(
                output,
                hook_text
            )


        except Exception as e:

            print(f"Hook failed: {e}")

            hooked_video = output


        print("Professional video completed.")

        return hooked_video


    except Exception as e:

        print(f"Video creation failed: {e}")

        return None
