import os
import requests


COGVIDEO_ENDPOINT = os.getenv("COGVIDEO_ENDPOINT")


def generate_cogvideo_video(prompt):

    print("=" * 60)
    print("COGVIDEO X")
    print("=" * 60)

    if not COGVIDEO_ENDPOINT:

        print("CogVideo endpoint not configured.")

        return None

    try:

        response = requests.post(

            COGVIDEO_ENDPOINT,

            json={

                "prompt": prompt

            },

            timeout=300

        )

        response.raise_for_status()

        result = response.json()

        video_url = extract_video(result)

        if video_url:

            print("COGVIDEO SUCCESS")

            return {

                "provider": "cogvideo",

                "url": video_url

            }

        print("CogVideo returned no usable video.")

        return None

    except Exception as e:

        print("=" * 60)
        print("COGVIDEO FAILED")
        print("=" * 60)
        print(e)

        return None


def extract_video(result):

    if result is None:

        return None

    if isinstance(result, str):

        if ".mp4" in result:

            return result

    if isinstance(result, dict):

        if "video" in result:

            if isinstance(result["video"], dict):

                return result["video"].get("url")

            return result["video"]

        if "url" in result:

            return result["url"]

    if isinstance(result, list):

        for item in result:

            url = extract_video(item)

            if url:

                return url

    return None
