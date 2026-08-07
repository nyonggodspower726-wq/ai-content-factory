import os
import requests

from config import PEXELS_API_KEY


PEXELS_URL = "https://api.pexels.com/v1/search"


def download_image(url, output_path):

    response = requests.get(
        url,
        timeout=60
    )

    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def generate_ai_image(
    prompt,
    output_folder="assets/images"
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    filename = (
        str(abs(hash(prompt)))
        + ".jpg"
    )

    image_path = os.path.join(
        output_folder,
        filename
    )

    if os.path.exists(image_path):

        print(
            "Using cached image:",
            image_path
        )

        return image_path

    headers = {

        "Authorization": PEXELS_API_KEY

    }

    params = {

        "query": prompt,

        "per_page": 1,

        "orientation": "portrait"

    }

    try:

        print("=" * 60)
        print("PEXELS IMAGE SEARCH")
        print("=" * 60)
        print("Searching:", prompt)

        response = requests.get(

            PEXELS_URL,

            headers=headers,

            params=params,

            timeout=60

        )

        response.raise_for_status()

        data = response.json()

        photos = data.get("photos", [])

        if len(photos) == 0:

            print("No Pexels image found.")

            return None

        image_url = photos[0]["src"]["large2x"]

        download_image(

            image_url,

            image_path

        )

        print(
            "Downloaded:",
            image_path
        )

        return image_path

    except Exception as e:

        print("=" * 60)
        print("PEXELS FAILED")
        print("=" * 60)
        print(e)

        return None
