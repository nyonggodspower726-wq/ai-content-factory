from gradio_client import Client
import time


SPACE_NAME = "Upsampler/wan-2-2-5b-video"



def generate_wan_video(prompt):

    print("=" * 60)
    print("WAN 2.2 VIDEO GENERATOR")
    print("=" * 60)


    try:

        print("Connecting to WAN Space...")


        client = Client(
            SPACE_NAME
        )


        print(
            "Generating WAN video..."
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
            "Processing WAN response..."
        )


        print(
            "WAN RAW RESPONSE:"
        )

        print(result)



        time.sleep(3)



        video_url = extract_video(result)



        if video_url:


            print(
                "WAN VIDEO SUCCESS"
            )


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

        print(
            str(e)
        )


        return None





def extract_video(result):


    if result is None:

        return None



    # ------------------------------
    # STRING RESPONSE
    # ------------------------------

    if isinstance(result, str):

        if ".mp4" in result:

            return result



        if "http" in result:

            return result



    # ------------------------------
    # DICTIONARY RESPONSE
    # ------------------------------

    if isinstance(result, dict):


        for key, value in result.items():


            if isinstance(value, str):

                if ".mp4" in value:

                    return value



            if isinstance(value, dict):


                if "url" in value:

                    return value["url"]



                if "path" in value:

                    return value["path"]




    # ------------------------------
    # LIST / TUPLE RESPONSE
    # ------------------------------

    if isinstance(result, (list, tuple)):


        for item in result:


            url = extract_video(item)


            if url:

                return url




    # ------------------------------
    # FILE OBJECT RESPONSE
    # ------------------------------

    if hasattr(result, "path"):

        return result.path



    if hasattr(result, "url"):

        return result.url



    return None
