from gradio_client import Client
import os


SPACE_NAME = "Wan-AI/Wan-2.2-I2V"


def generate_wan_video(prompt):

    print("Connecting to Hugging Face Wan...")

    try:

        hf_token = os.getenv("HF_API_TOKEN")


        if not hf_token:
            print("HF token missing")
            return None


        client = Client(
            SPACE_NAME,
            token=hf_token
        )


        result = client.predict(
            prompt,
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


    # limit to avoid Railway overload

    prompts = prompts[:6]


    for index, prompt in enumerate(prompts):

        print("=" * 50)
        print(f"Generating Scene {index + 1}")
        print("=" * 50)


        video = generate_wan_video(prompt)


        if video:

            videos.append(video)

        else:

            print(
                f"Scene {index + 1} failed"
            )


    return videos
