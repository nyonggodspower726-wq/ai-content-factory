import os
import requests
import time

FAL_API_KEY = os.getenv("FAL_API_KEY")

MODEL = "minimax/h3/text-to-video"


def generate_fal_video(prompt):

    headers = {
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "duration": 5,
        "resolution": "720p",
        "aspect_ratio": "16:9"
    }

    # Submit job
    response = requests.post(
        f"https://queue.fal.run/{MODEL}",
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    request_id = response.json()["request_id"]

    print("Job Submitted:", request_id)

    # Wait for completion
    while True:

        status = requests.get(
            f"https://queue.fal.run/{MODEL}/requests/{request_id}/status",
            headers=headers
        ).json()

        if status["status"] == "COMPLETED":
            break

        if status["status"] == "FAILED":
            return None

        print("Generating...")
        time.sleep(5)

    # Fetch result
    result = requests.get(
        f"https://queue.fal.run/{MODEL}/requests/{request_id}",
        headers=headers
    ).json()

    return result["video"]["url"]
