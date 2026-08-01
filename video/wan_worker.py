import requests
from config import HUGGINGFACE_TOKEN

# We will update this to the exact Wan Video model later
MODEL_URL = "https://api-inference.huggingface.co/models"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}


def generate_wan_video(prompt):

    print("Generating AI video with Wan...")

    payload = {
        "inputs": prompt
    }

    try:

        response = requests.post(
            MODEL_URL,
            headers=HEADERS,
            json=payload,
            timeout=600
        )

        print(response.status_code)

        return response

    except Exception as e:

        print(e)

        return None
