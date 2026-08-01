import os
import requests


WAN_API_URL = os.getenv(
    "WAN_API_URL"
)


def generate_wan_video(
    prompt,
    duration=5
):

    print("Wan Video generating scene...")
    print(prompt)


    if not WAN_API_URL:

        print(
            "Wan Video worker not connected"
        )

        return None


    payload = {

        "prompt": prompt,

        "duration": duration,

        "width": 1080,

        "height": 1920,

        "fps": 24

    }


    try:

        response = requests.post(

            WAN_API_URL,

            json=payload,

            timeout=600

        )


        response.raise_for_status()


        data = response.json()


        return data.get(
            "video_url"
        )


    except Exception as e:

        print(
            f"Wan generation failed: {e}"
        )

        return None
