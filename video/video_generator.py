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
        "per_page": 5
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if "videos" in data and data["videos"]:

        for video in data["videos"]:
            for file in video["video_files"]:
                if file.get("width", 0) >= 720:
                    return file["link"]

    return None



def download_video(url):

    os.makedirs("output", exist_ok=True)

    path = "output/background.mp4"

    r = requests.get(url)

    with open(path, "wb") as f:
        f.write(r.content)

    return path



def create_video(script, voice_file):

    print("Creating professional AI video...")


    keywords = [
        word for word in script.split()
        if len(word) > 4
    ]

    search_term = " ".join(keywords[:4])

    print(f"Searching Pexels: {search_term}")


    video_url = search_pexels_video(search_term)

    if not video_url:
        print("No background video found.")
        return None


    background = download_video(video_url)

    print("Background downloaded.")


    try:

        video = VideoFileClip(background)

        audio = AudioFileClip(voice_file)


        # Vertical format
        video = video.resize(height=1280)

        video = video.crop(
            x_center=video.w/2,
            y_center=video.h/2,
            width=720,
            height=1280
        )


        video = video.set_duration(audio.duration)


        final = video.set_audio(audio)


        output = "output/final_video.mp4"


        final.write_videofile(
            output,
            fps=24,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=1
        )


        print("Professional video created.")

        return output


    except Exception as e:

        print(f"Video creation failed: {e}")

        return None
