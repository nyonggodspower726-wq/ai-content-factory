import os
import requests


LTX_API = os.getenv("LTX_API_KEY")


def generate_ltx_video(prompt):

    print("=" * 60)
    print("LTX VIDEO")
    print("=" * 60)

    if not LTX_API:

        print("LTX API not configured.")

        return None

    try:

        response = requests.post(

            "YOUR_LTX_ENDPOINT",

            headers={

                "Authorization": f"Bearer {LTX_API}"

            },

            json={

                "prompt": prompt

            },

            timeout=120

        )

        response.raise_for_status()

        data = response.json()

        return data

    except Exception as e:

        print("LTX failed")

        print(e)

        return None
