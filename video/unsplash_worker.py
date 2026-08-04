import os
import requests


UNSPLASH_API = os.getenv("UNSPLASH_ACCESS_KEY")


def generate_unsplash_video(prompt):

    print("=" * 60)
    print("UNSPLASH FALLBACK")
    print("=" * 60)

    if not UNSPLASH_API:

        print("Unsplash API not configured.")

        return None

    try:

        response = requests.get(

            "https://api.unsplash.com/photos/random",

            headers={

                "Authorization": f"Client-ID {UNSPLASH_API}"

            },

            params={

                "query": prompt

            },

            timeout=60

        )

        response.raise_for_status()

        data = response.json()

        return {

            "url": data["urls"]["regular"]

        }

    except Exception as e:

        print(e)

        return None
