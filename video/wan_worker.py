from gradio_client import Client
import os


SPACE_NAME = "Wan-AI/Wan-2.2-I2V"


def generate_wan_video(prompt):

    print("Connecting to Hugging Face Wan...")

    try:

        hf_token = os.getenv("HF_API_TOKEN")

        client = Client(
            SPACE_NAME,
            hf_token=hf_token
        )


        result = client.predict(
            prompt=prompt,
            api_name="/predict"
        )


        if isinstance(result, str):

            return result


        if isinstance(result, (list, tuple)):

            for item in result:

                if isinstance(item, str):

                    return item


        return None


    except Exception as e:

        print(
            f"Wan generation error: {e}"
        )

        return None



def generate_all_scenes(prompts):

    videos = []

    for prompt in prompts:

        video = generate_wan_video(prompt)

        if video:

            videos.append(video)

    return videos
