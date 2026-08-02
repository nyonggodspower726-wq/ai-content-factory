from gradio_client import Client
import os
import time


SPACE_Surrendara1991 = "Wan-AI/Wan-2.2-I2V-A14B


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



def generate_all_scenes(prompts):

    videos = []


    # Keep maximum 6 scenes
    prompts = prompts[:6]


    for index, prompt in enumerate(prompts):

        print("=" * 60)
        print(f"GENERATING SCENE {index + 1}")
        print("=" * 60)


        # Retry failed scene twice

        attempts = 0
        video = None


        while attempts < 3 and not video:

            attempts += 1

            print(
                f"Scene {index + 1} attempt {attempts}"
            )


            video = generate_wan_video(prompt)


            if not video:

                print(
                    "Retrying..."
                )

                time.sleep(5)



        if video:

            print(
                f"Scene {index + 1} completed"
            )

            videos.append(video)


        else:

            print(
                f"Scene {index + 1} failed after retries"
            )



    return videos
