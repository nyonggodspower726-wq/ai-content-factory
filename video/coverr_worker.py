import requests

from config import (
    COVERR_API_KEY,
    COVERR_API_URL
)


# ============================================================
# COVERR VIDEO PROVIDER
# ============================================================

def generate_coverr_video(prompt):

    if not COVERR_API_KEY:

        print("=" * 60)
        print("COVERR API KEY MISSING")
        print("=" * 60)

        return None

    try:

        print("=" * 60)
        print("SEARCHING COVERR")
        print("=" * 60)

        headers = {
            "Authorization": f"Bearer {COVERR_API_KEY}",
            "Accept": "application/json"
        }

        params = {
            "query": prompt,
            "page": 0,
            "page_size": 1,
            "urls": "true"
        }

        response = requests.get(
            COVERR_API_URL,
            headers=headers,
            params=params,
            timeout=60
        )

        print(f"Coverr Status: {response.status_code}")

        response.raise_for_status()

        data = response.json()

        print("Coverr Response:")
        print(data)

        videos = data.get("hits", [])

        if len(videos) == 0:

            print("No Coverr videos found.")

            return None

        video = videos[0]

        # Try all possible download locations
        urls = video.get("urls", {})

        video_url = (
            urls.get("mp4_download")
            or urls.get("download")
            or urls.get("preview")
            or video.get("download_url")
            or video.get("video_url")
            or video.get("url")
        )

        if not video_url:

            print("No downloadable video URL found.")

            return None

        print("Coverr video found.")
        print(video_url)

        return video_url

    except requests.HTTPError as e:

        print("=" * 60)
        print("COVERR HTTP ERROR")
        print("=" * 60)
        print(e)

        if e.response is not None:
            print(e.response.text)

        return None

    except Exception as e:

        print("=" * 60)
        print("COVERR FAILED")
        print("=" * 60)
        print(e)

        return None
