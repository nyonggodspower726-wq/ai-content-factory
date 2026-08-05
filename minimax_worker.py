import os
from gradio_client import Client


# MiniMax Hugging Face Space
SPACE_NAME = "adahling305/minimax-h3-demo"


def generate_minimax_video(prompt):

    print("=" * 60)
    print("MINIMAX H3 VIDEO GENERATOR")
    print("=" * 60)

    try:

        print("Connecting to MiniMax Space...")

        client = Client(
            SPACE_NAME
        )


        print("Generating video...")

        result = client.predict(

            prompt=prompt,

            canvas="960x544 - 16:9 fast",

            duration=2,

            steps=12,

            seed=42,

            api_name="/generate"

        )


        print("Processing MiniMax result...")


        video_url = extract_video(result)


        if video_url:

            print("MINIMAX SUCCESS")

            return video_url


        print(
            "MiniMax returned no video"
        )

        return None


    except Exception as e:

        print(
            "MINIMAX ERROR:"
        )

        print(e)

        return None



def extract_video(result):


    # Direct URL

    if isinstance(result, str):

        if result.endswith(".mp4"):

            return result



    # List response

    if isinstance(result, list):

        for item in result:


            if isinstance(item, str):

                if ".mp4" in item:

                    return item



            if isinstance(item, dict):


                if "video" in item:

                    return item["video"]


                if "url" in item:

                    return item["url"]



    # Dictionary response

    if isinstance(result, dict):


        if "video" in result:

            return result["video"]


        if "url" in result:

            return result["url"]



    return None
