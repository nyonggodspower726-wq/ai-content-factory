import requests


COGVIDEO_ENDPOINT = ""


def generate_cogvideo_video(prompt):

    print("=" * 60)
    print("COGVIDEO X")
    print("=" * 60)

    if COGVIDEO_ENDPOINT == "":

        print("CogVideo endpoint not configured.")

        return None

    try:

        response = requests.post(

            COGVIDEO_ENDPOINT,

            json={

                "prompt": prompt

            },

            timeout=300

        )

        response.raise_for_status()

        result = response.json()

        if isinstance(result, dict):

            if "video" in result:

                return result["video"]

            if "url" in result:

                return result["url"]

        return None

    except Exception as e:

        print("COGVIDEO ERROR")

        print(str(e))

        return None
