import os
import requests
import time


VIDEO_MODEL_URL = os.getenv(
    "VIDEO_MODEL_URL"
)


def generate_video_scene(prompt, duration=5):

    print("AI Video Worker Started")
    print(prompt)


    if not VIDEO_MODEL_URL:

        print(
            "No video model worker connected."
        )

        return None


    payload = {

        "prompt": prompt,

        "duration": duration,

        "aspect_ratio": "9:16",

        "quality": "high"

    }


    try:

        response = requests.post(

            VIDEO_MODEL_URL,

            json=payload,

            timeout=300

        )


        response.raise_for_status()


        data = response.json()


        return data.get(
            "video_url"
        )


    except Exception as e:

        print(
            f"Worker error: {e}"
        )

        return None



def generate_all_scenes(prompts):

    videos = []


    for index, prompt in enumerate(prompts):

        print(
            f"Generating scene {index+1}"
        )


        video = generate_video_scene(
            prompt
        )


        if video:

            videos.append(video)


        time.sleep(2)


    return videos
