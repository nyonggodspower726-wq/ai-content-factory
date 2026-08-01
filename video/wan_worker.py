from gradio_client import Client
import tempfile
import shutil
import os

SPACE_NAME = "Wan-AI/Wan-2.2-I2V"


def generate_wan_video(prompt):

    print("Connecting to Hugging Face Wan...")

    try:

        client = Client(SPACE_NAME)

        result = client.predict(

            prompt=prompt,

            api_name="/predict"

        )

        if isinstance(result, str):

            return result

        return None

    except Exception as e:

        print(e)

        return None


def generate_all_scenes(prompts):

    videos = []

    for prompt in prompts:

        video = generate_wan_video(prompt)

        if video:

            videos.append(video)

    return videos
