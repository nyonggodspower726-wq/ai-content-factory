from gradio_client import Client
import os


SPACE_NAME = "Wan-AI/Wan-2.2-I2V"


def generate_wan_video(prompt):

    print("=" * 50)
    print("Connecting to Hugging Face Wan...")
    print("=" * 50)

    try:

        client = Client(
            SPACE_NAME
        )


        result = client.predict(
            prompt=prompt,
            api_name="/predict"
        )


        print(
            "Wan response received:"
        )

        print(
            result
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
            "Wan video generation failed:"
        )

        print(
            str(e)
        )

        return None



def generate_all_scenes(prompts):

    videos = []


    for index, prompt in enumerate(prompts):

        print(
            f"Generating scene {index + 1}"
        )


        video = generate_wan_video(
            prompt
        )


        if video:

            videos.append(video)

        else:

            print(
                f"Scene {index + 1} failed"
            )


    return videos
