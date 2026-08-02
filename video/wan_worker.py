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

        result = client.predict(
            prompt,
            2,
            api_name="/predict"
        )

        if isinstance(result, str):
            return result

        if isinstance(result, (list, tuple)):

            for item in result:
                if isinstance(item, str):
                    return item

        print("Wan returned no video")

        return None


    except Exception as e:

        print(
            f"WAN ERROR: {e}"
        )

        return None
