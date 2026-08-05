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

        print("=" * 60)
        print(f"Coverr Status: {response.status_code}")
        print("=" * 60)

        print("Response Body:")
        print(response.text)

        response.raise_for_status()

        data = response.json()

        print("=" * 60)
        print("Coverr JSON Response")
        print("=" * 60)
        print(data)

        videos = data.get("hits", [])

        if not videos:

            print("No Coverr videos found.")

            return None

        video = videos[0]

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

        print("=" * 60)
        print("COVERR VIDEO FOUND")
        print("=" * 60)
        print(video_url)

        return video_url

    except requests.HTTPError as e:

        print("=" * 60)
        print("COVERR HTTP ERROR")
        print("=" * 60)

        print(e)

        if e.response is not None:

            print("Status:", e.response.status_code)
            print("Body:")
            print(e.response.text)

        return None

    except Exception as e:

        print("=" * 60)
        print("COVERR FAILED")
        print("=" * 60)

        print(e)

        return None
