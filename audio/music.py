import os
import requests
import random

from config import PIXABAY_API_KEY


def get_music():

    print("Searching Pixabay music...")

    os.makedirs(
        "output/music",
        exist_ok=True
    )

    url = "https://pixabay.com/api/"

    params = {
        "key": PIXABAY_API_KEY,
        "q": "motivational cinematic background",
        "media_type": "music",
        "per_page": 20,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "hits" not in data or len(data["hits"]) == 0:

            print("No music found.")

            return None


        music = random.choice(
            data["hits"]
        )


        music_url = music.get(
            "audio"
        )


        if not music_url:

            print("No audio URL found.")

            return None


        file_path = (
            "output/music/"
            "background_music.mp3"
        )


        print("Downloading music...")


        audio = requests.get(
            music_url,
            timeout=60
        )


        audio.raise_for_status()


        with open(
            file_path,
            "wb"
        ) as f:

            f.write(
                audio.content
            )


        print(
            "Background music downloaded:",
            file_path
        )


        return file_path


    except Exception as e:

        print(
            "Music download failed:",
            e
        )

        return None
