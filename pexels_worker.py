import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def generate_pexels_video(prompt):

    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY not found")
        return None

    try:

        headers = {
            "Authorization": PEXELS_API_KEY
        }

        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params={
                "query": prompt,
                "per_page": 3
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        if not data.get("videos"):
            return None

        urls = []

        for video in data["videos"]:

            files = video.get("video_files", [])

            if not files:
                continue

            best = max(files, key=lambda x: x.get("width", 0))

            urls.append({
                "provider": "pexels",
                "url": best["link"]
            })

        return urls

    except Exception as e:

        print("PEXELS ERROR")
        print(e)

        return None
