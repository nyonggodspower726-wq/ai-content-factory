import os
import requests

from config import PEXELS_API_KEY


def search_pexels_video(query):

    url = "https://api.pexels.com/videos/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 1
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    if "videos" in data and len(data["videos"]) > 0:

        video_files = data["videos"][0]["video_files"]

        return video_files[0]["link"]

    return None



def download_video(url):

    os.makedirs("output", exist_ok=True)

    file_path = "output/background.mp4"

    response = requests.get(url)

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path



def create_video(script):

    print("Creating AI video...")

    # Simple keyword search for now
    keywords = script.split(" ")[0:5]
    search_term = " ".join(keywords)

    print(f"Searching Pexels: {search_term}")

    video_url = search_pexels_video(search_term)

    if not video_url:
        print("No Pexels video found.")
        return None

    video = download_video(video_url)

    print("Background video downloaded.")

    return video
