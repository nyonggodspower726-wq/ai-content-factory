import os
import requests

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip
)

from config import PEXELS_API_KEY



def search_pexels_video(query):

    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if "videos" in data and len(data["videos"]) > 0:

        files = data["videos"][0]["video_files"]

        return files[0]["link"]

    return None



def download_video(url):

    os.makedirs("output", exist_ok=True)

    path = "output/background.mp4"

    response = requests.get(url)

    with open(path, "wb") as file:
        file.write(response.content)

    return path



def create_video(script, voice_file="output/voice.mp3"):

    print("Creating AI video...")

    words = script.split(" ")[0:5]
    search_term = " ".join(words)

    print(f"Searching Pexels: {search_term}")

    video_url = search_pexels_video(search_term)

    if not video_url:
        print("No video found.")
        return None


    background = download_video(video_url)

    print("Background video downloaded.")


    try:

        video = VideoFileClip(background)

        audio = AudioFileClip(voice_file)


        # Resize for TikTok/Reels/Shorts
        video = video.resize(height=1920)

        video = video.crop(
            width=1080,
            height=1920,
            x_center=video.w / 2,
            y_center=video.h / 2
        )


        # Match video length to voice
        video = video.set_duration(
            min(video.duration, audio.duration)
        )


        final = video.set_audio(audio)


        output = "output/final_video.mp4"

        final.write_videofile(
            output,
            fps=30,
            codec="libx264",
            audio_codec="aac"
        )


        print("Final video created.")

        return output


    except Exception as e:

        print(f"Video creation failed: {e}")

        return None
