import os
import time
import requests

FAL_API_KEY = os.getenv("FAL_KEY")

MODEL = "minimax/h3/text-to-video"

BASE_URL = f"https://fal.run/{MODEL}"


def generate_minimax_video(
    prompt,
    duration=5,
    resolution="2K",
    aspect_ratio="16:9"
):

    if not FAL_API_KEY:
        print("FAL API KEY NOT FOUND")
        return None

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "duration": duration,
        "resolution": resolution,
        "aspect_ratio": aspect_ratio
    }

    try:

        print("=" * 60)
        print("MINIMAX H3")
        print("=" * 60)

        response = requests.post(
            BASE_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        result = response.json()

        if "video" in result:

            video = result["video"]

            if isinstance(video, dict):

                url = video.get("url")

                if url:
                    print("MiniMax video generated.")
                    return url

        print(result)

        return None

    except Exception as e:

        print(f"MiniMax Error: {e}")

        return None
