from gradio_client import Client
import os
import time


SPACE_NAME = "Upsampler/wan-2-2-5b-video"



def generate_wan_video(prompt):

    print("=" * 50)
    print("WAN VIDEO GENERATOR")
    print("=" * 50)


    try:

        hf_token = os.getenv(
            "HF_API_TOKEN"
        )


        if not hf_token:

            print(
                "HF TOKEN NOT FOUND"
            )

            return None



        print(
            "Connecting to WAN..."
        )


        client = Client(

            SPACE_NAME,

            hf_token=hf_token

        )



        print(
            "Generating video..."
        )


        result = client.predict(

            input_image=None,

            prompt=prompt,

            height=896,

            width=896,

            negative_prompt=(
                "overexposed, blurry, "
                "low quality, distorted"
            ),

            duration_seconds=2,

            guidance_scale=0,

            steps=4,

            seed=42,

            randomize_seed=True,

            api_name="/generate_video"

        )



        print(
            "Processing WAN result..."
        )


        time.sleep(5)



        video_url = extract_video(result)



        if video_url:

            print(
                "WAN VIDEO SUCCESS"
            )

            return video_url



        print(
            "WAN returned no video"
        )


        return None



    except Exception as e:


        print(
            "WAN ERROR:"
        )

        print(e)


        return None




def extract_video(result):


    if isinstance(result, str):

        if result.endswith(".mp4"):

            return result



    if isinstance(result, list):


        for item in result:


            if isinstance(item, str):

                if item.endswith(".mp4"):

                    return item



            if isinstance(item, dict):


                if "video" in item:

                    return item["video"]



                if "url" in item:

                    return item["url"]



    return None
