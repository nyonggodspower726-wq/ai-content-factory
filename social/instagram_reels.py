import os
import time
import requests

INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_API_VERSION = os.getenv("INSTAGRAM_API_VERSION", "v23.0")
INSTAGRAM_BASE_URL = f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}"


def upload_to_instagram(video_url, caption=""):
    print("=" * 60)
    print("INSTAGRAM DIRECT API UPLOADER")
    print("=" * 60)

    if not INSTAGRAM_ACCOUNT_ID:
        raise RuntimeError("INSTAGRAM_ACCOUNT_ID is not configured in Railway Variables.")

    if not INSTAGRAM_ACCESS_TOKEN:
        raise RuntimeError("INSTAGRAM_ACCESS_TOKEN is not configured in Railway Variables.")

    if not video_url:
        raise ValueError("No public video URL provided.")

    # Step 1: create Reel container
    response = requests.post(
        f"{INSTAGRAM_BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media",
        data={
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=120,
    )

    print("Container HTTP status:", response.status_code)
    print("Container response:", response.text)

    if not response.ok:
        raise RuntimeError(
            "Instagram container creation failed: " + response.text
        )

    data = response.json()
    container_id = data.get("id")

    if not container_id:
        raise RuntimeError(
            f"Instagram did not return a container ID: {data}"
        )

    print("Instagram container ID:", container_id)

    # Step 2: wait for processing
    for attempt in range(1, 31):
        status_response = requests.get(
            f"{INSTAGRAM_BASE_URL}/{container_id}",
            params={
                "fields": "status_code,status",
                "access_token": INSTAGRAM_ACCESS_TOKEN,
            },
            timeout=60,
        )

        print(
            f"Processing check {attempt}/30:",
            status_response.text
        )

        if not status_response.ok:
            raise RuntimeError(
                "Instagram container status check failed: "
                + status_response.text
            )

        status_data = status_response.json()
        status_code = status_data.get("status_code")

        if status_code == "FINISHED":
            break

        if status_code in ("ERROR", "EXPIRED"):
            raise RuntimeError(
                "Instagram video processing failed: "
                + str(status_data)
            )

        time.sleep(5)

    else:
        raise RuntimeError("Instagram video processing timed out.")

    # Step 3: publish Reel
    publish_response = requests.post(
        f"{INSTAGRAM_BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": INSTAGRAM_ACCESS_TOKEN,
        },
        timeout=120,
    )

    print("Publish HTTP status:", publish_response.status_code)
    print("Publish response:", publish_response.text)

    if not publish_response.ok:
        raise RuntimeError(
            "Instagram Reel publish failed: " + publish_response.text
        )

    result = publish_response.json()

    print("=" * 60)
    print("INSTAGRAM REEL PUBLISHED SUCCESSFULLY")
    print("=" * 60)
    print(result)

    return result
    
