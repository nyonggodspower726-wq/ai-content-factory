import os
import requests
import PIL.Image

# Fix MoviePy + Pillow compatibility
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS


from moviepy.editor import VideoFileClip, AudioFileClip

from config import PEXELS_API_KEY
from video.subtitle_generator import create_subtitles



def search_pexels_video(query):

    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 10
    }

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

                    link = file.get("link", "")

                    if (
                        link.endswith(".mp4")
                        and file.get("width", 0) >= 720
                    ):
                        return link

    except Exception as e:

        print(f"Pexels search failed: {e}")

    return None



def download_video(url):

    os.makedirs("output", exist_ok=True)

    path = "output/background.mp4"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

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

    print("Video file downloaded.")

    return path



def create_video(script, voice_file):

    print("Creating professional AI video...")


    keywords = [
        word
        for word in script.split()
        if len(word) > 4
    ]

    search_term = " ".join(keywords[:4])


    print(f"Searching Pexels: {search_term}")


    video_url = search_pexels_video(search_term)


    if not video_url:

        print("No background video found.")

        return None



    background = download_video(video_url)


    try:

        video = VideoFileClip(background)

        audio = AudioFileClip(voice_file)


        # Vertical format for TikTok/Reels/Shorts
        video = video.resize(height=1280)


        video = video.crop(
            x_center=video.w / 2,
            y_center=video.h / 2,
            width=720,
            height=1280
        )


        # Match video length with voice
        video = video.set_duration(
            audio.duration
        )


        # Create subtitle file (.srt)
        create_subtitles(script)


        # Keep final video clip
        final = video.set_audio(audio)


        output = "output/final_video.mp4"


        final.write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="ultrafast",
            threads=1,
            logger=None
        )


        print("Professional video created.")


        return output



    except Exception as e:

        print(f"Video creation failed: {e}")

        return None
