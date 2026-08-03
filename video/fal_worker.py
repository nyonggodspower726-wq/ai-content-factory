import os
import time
import requests


FAL_API_KEY = os.getenv("FAL_API_KEY")

# We'll replace this endpoint with the exact model later
FAL_ENDPOINT = "https://fal.run/fal-ai/wan"


def generate_fal_video(prompt):

    print("=" * 60)
    print("FAL.AI VIDEO")
    print("=" * 60)

    if not FAL_API_KEY:

        print("FAL API KEY NOT FOUND")

        return None


    headers = {

        "Authorization": f"Key {FAL_API_KEY}",

        "Content-Type": "application/json"

    }


    payload = {

        "prompt": prompt

    }


    try:

        response = requests.post(

            FAL_ENDPOINT,

            headers=headers,

            json=payload,

            timeout=300

        )


        response.raise_for_status()


        result = response.json()


        print(result)


        return result


    except Exception as e:

        print("FAL ERROR")

        print(str(e))

        return None
