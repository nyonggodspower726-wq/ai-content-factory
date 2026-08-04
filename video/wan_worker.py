from gradio_client import Client
import time


SPACE_NAME = "Upsampler/wan-2-2-5b-video"


def generate_wan_video(prompt):

    print("=" * 60)
    print("WAN 2.2 VIDEO GENERATOR")
    print("=" * 60)

    try:

        print("Connecting to WAN Space...")

        # Removed hf_token because Railway gradio_client rejects it
        client = Client(
            SPACE_NAME
        )


        print("Generating WAN video...")


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


        print("Processing WAN response...")


        time.sleep(3)


        video_url = extract_video(result)


        if video_url:

            print("WAN VIDEO SUCCESS")


            return {

                "provider": "wan",

                "url": video_url

            }


        print(
            "WAN returned no usable video."
        )

        return None



    except Exception as e:


        print("=" * 60)
        print("WAN FAILED")
        print("=" * 60)

        print(str(e))


        return None




def extract_video(result):


    if result is None:

        return None



    # String response

    if isinstance(result, str):

        if ".mp4" in result:

            return result



    # Dictionary response

    if isinstance(result, dict):


        if "video" in result:


            if isinstance(result["video"], dict):

                return result["video"].get(
                    "url"
                )


            return result["video"]



        if "url" in result:

            return result["url"]




    # List response

    if isinstance(result, list):


        for item in result:


            url = extract_video(item)


            if url:

                return url



    return None
