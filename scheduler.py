from gradio_client import Client
import os
import time


SPACE_NAME = "Upsampler/wan-2-2-5b-video"


def generate_wan_video(prompt):

    print("Connecting to Hugging Face Wan...")

    try:

        hf_token = os.getenv("HF_API_TOKEN")

        if not hf_token:
            print("HF TOKEN NOT FOUND")
            return None


        print("HF TOKEN FOUND")


        client = Client(
            SPACE_NAME,
            token=hf_token
        )


        print("Getting available API...")


        result = client.predict(
            prompt,
            2,
            api_name="/generate"
        )


        if isinstance(result, str):
            return result


        if isinstance(result, (list, tuple)):

            for item in result:
                if isinstance(item, str):
                    return item


        print("No video returned")

        return None


    except Exception as e:

        print(f"WAN ERROR: {e}")

        return None



def generate_all_scenes(prompts):

    videos = []

    prompts = prompts[:6]


    for index, prompt in enumerate(prompts):

        print("="*50)
        print(f"GENERATING SCENE {index+1}")
        print("="*50)


        attempts = 0
        video = None


        while attempts < 3 and not video:

            attempts += 1

            video = generate_wan_video(prompt)


            if not video:
                time.sleep(5)


        if video:
            videos.append(video)

        else:
            print(f"Scene {index+1} failed")


    return videos
