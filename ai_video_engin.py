import os
import requests

from config import AI_VIDEO_API_KEY


def generate_scene(prompt, duration=5):

    print("Generating AI video scene...")
    print(prompt)

    # This is the connection point
    # for your future AI video model

    api_url = os.getenv(
        "AI_VIDEO_API_URL"
    )

    if not api_url:

        print(
            "AI video engine not connected yet."
        )

        return None


    headers = {

        "Authorization":
        f"Bearer {AI_VIDEO_API_KEY}",

        "Content-Type":
        "application/json"

    }


    payload = {

        "prompt": prompt,

        "duration": duration,

        "quality": "cinematic",

        "aspect_ratio": "9:16"

    }


    try:

        response = requests.post(

            api_url,

            headers=headers,

            json=payload,

            timeout=120

        )


        response.raise_for_status()


        data = response.json()


        return data.get(
            "video_url"
        )


    except Exception as e:

        print(
            f"AI video generation failed: {e}"
        )

        return None



def generate_scenes(prompts):

    scenes = []


    for scene in prompts:

        video = generate_scene(
            scene
        )

        if video:

            scenes.append(video)


    return scenes
