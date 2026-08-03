import requests


LTX_ENDPOINT = ""


def generate_ltx_video(prompt):

    print("=" * 60)
    print("LTX VIDEO")
    print("=" * 60)

    if LTX_ENDPOINT == "":

        print("LTX endpoint not configured.")

        return None

    try:

        response = requests.post(

            LTX_ENDPOINT,

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

        print("LTX ERROR")

        print(str(e))

        return None
