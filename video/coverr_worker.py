import os
import requests


COVERR_API_KEY = os.getenv("COVERR_API_KEY")


def generate_coverr_video(prompt):

    if not COVERR_API_KEY:

        print("Coverr API key missing")

        return None


    try:

        url = "https://api.coverr.co/videos"


        headers = {
            "Authorization": COVERR_API_KEY
        }


        params = {
            "query": prompt,
            "page": 1,
            "page_size": 1
        }


        response = requests.get(

            url,

            headers=headers,

            params=params,

            timeout=60

        )


        response.raise_for_status()


        data = response.json()


        videos = data.get(
            "hits",
            []
        )


        if not videos:

            print(
                "No Coverr videos found"
            )

            return None


        video_url = videos[0].get(
            "url"
        )


        if video_url:

            print(
                "Coverr video found"
            )

            return video_url



    except Exception as e:

        print(
            "Coverr error:",
            e
        )


    return None
