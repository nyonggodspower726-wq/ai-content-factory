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
            hf_token=hf_token
        )

        print("Generating video...")

        result = client.predict(
            input_image=None,
            prompt=prompt,
            height=896,
            width=896,
            negative_prompt="Bright tones, overexposed, static, blurry details",
            duration_seconds=2,
            guidance_scale=0,
            steps=4,
            seed=42,
            randomize_seed=True,
            api_name="/generate_video"
        )

        print("Waiting for WAN output...")
        time.sleep(30)

        if isinstance(result, str):
            print("Video received")
            return result

        if isinstance(result, list):

            for item in result:

                if isinstance(item, str) and item.endswith(".mp4"):
                    print("Video received")
                    return item

                if isinstance(item, dict):
                    if "video" in item:
                        return item["video"]

                    if "url" in item:
                        return item["url"]

        print(result)
        print("No video returned")
        return None

    except Exception as e:

        print(f"WAN ERROR: {e}")
        return None


def generate_all_scenes(prompts):

    videos = []

    prompts = prompts[:6]

    for index, prompt in enumerate(prompts):

        print("=" * 60)
        print(f"GENERATING SCENE {index + 1}")
        print("=" * 60)

        attempts = 0
        video = None

        while attempts < 3 and not video:

            attempts += 1

            print(f"Attempt {attempts}")

            video = generate_wan_video(prompt)

            if not video:
                print("Retrying in 10 seconds...")
                time.sleep(10)

        if video:

            print(f"Scene {index + 1} completed")
            videos.append(video)

        else:

            print(f"Scene {index + 1} failed")

    return videos
