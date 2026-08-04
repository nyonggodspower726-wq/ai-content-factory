import os
import requests


PEXELS_API = os.getenv("PEXELS_API_KEY")


def generate_pexels_video(prompt):

    print("=" * 60)
    print("PEXELS FALLBACK")
    print("=" * 60)

    if not PEXELS_API:

        print("Pexels API not configured.")

        return None

    try:

        response = requests.get(

            "https://api.pexels.com/videos/search",

            headers={

                "Authorization": PEXELS_API

            },

            params={

                "query": prompt,

                "per_page": 1

            },

            timeout=60

        )

        response.raise_for_status()

        data = response.json()

        videos = data.get("videos", [])

        if not videos:

            return None

        return {

            "url": videos[0]["video_files"][0]["link"]

        }

    except Exception as e:

        print(e)

        return None
