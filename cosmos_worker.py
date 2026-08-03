import os
import requests


NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

# Replace with the correct NVIDIA video generation endpoint
NVIDIA_URL = "YOUR_NVIDIA_VIDEO_ENDPOINT"


def generate_cosmos_video(prompt):

    print("=" * 60)
    print("NVIDIA COSMOS")
    print("=" * 60)

    if not NVIDIA_API_KEY:

        print("NVIDIA API KEY NOT FOUND")

        return None

    headers = {

        "Authorization": f"Bearer {NVIDIA_API_KEY}",

        "Content-Type": "application/json"

    }

    payload = {

        "prompt": prompt

    }

    try:

        response = requests.post(

            NVIDIA_URL,

            headers=headers,

            json=payload,

            timeout=300

        )

        response.raise_for_status()

        result = response.json()

        print("NVIDIA generation completed.")

        return result

    except Exception as e:

        print("NVIDIA Cosmos Error")

        print(str(e))

        return None
