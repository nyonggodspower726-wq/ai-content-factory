import os
import requests
import PIL.Image

# Fix MoviePy + Pillow compatibility
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS


from moviepy.editor import VideoFileClip, AudioFileClip

from config import PEXELS_API_KEY



def search_pexels_video(query):

    print(f"Searching Pexels: {query}")

    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY,
        "User-Agent": "Mozilla/5.0"
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

                    link = file.get("link")

                    width = file.get("width", 0)

                    if link and width >= 720:
                        return link

        return None


    except Exception as e:

        print(f"Pexels search error: {e}")

        return None




def download_video(url):

    os.makedirs("output", exist_ok=True)

    path = "output/background.mp4"


    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }


        response = requests.get(
            url,
            headers=headers,
            stream=True,
            timeout=60
        )


        with open(path, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=1024 * 1024
            ):

                if chunk:
                    file.write(chunk)


        print("Video file downloaded.")

        return path


    except Exception as e:

        print(f"Download error: {e}")

        return None





def create_video(script, voice_file):

    print("Creating professional AI video...")


    # Better search words
    words = [
        word for word in script.split()
        if len(word) > 5
    ]


    search_term = " ".join(words[:4])


    video_url = search_pexels_video(search_term)


    if not video_url:

        print("No Pexels video found.")

        return None



    background = download_video(video_url)


    if not background:

        return None



    print("Background downloaded.")



    try:


        video = VideoFileClip(background)


        audio = AudioFileClip(voice_file)



        # TikTok / Shorts vertical format

        video = video.resize(height=1280)


        video = video.crop(
            x_center=video.w / 2,
            y_center=video.h / 2,
            width=720,
            height=1280
        )



        # Match voice duration

        video = video.set_duration(
            audio.duration
        )



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
