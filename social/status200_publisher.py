import os
import requests


STATUS200_API_KEY = os.getenv("STATUS200_API_KEY")
TIKTOK_ACCOUNT = os.getenv(
    "STATUS200_TIKTOK_ACCOUNT",
    "@Promptprohub"
)

BASE_URL = "https://app.status200uploads.com/functions/v1"


def publish_to_tiktok(video_url, caption):
    """
    Upload a publicly accessible video URL to Status 200
    and publish it to the connected TikTok account.
    """

    if not STATUS200_API_KEY:
        raise RuntimeError(
            "STATUS200_API_KEY is not configured."
        )

    if not video_url:
        raise ValueError(
            "No video URL provided."
        )

    headers = {
        "Authorization": f"Bearer {STATUS200_API_KEY}",
        "Content-Type": "application/json",
    }

    # -----------------------------
    # STEP 1: Upload media
    # -----------------------------

    print("=" * 60)
    print("STATUS 200 MEDIA UPLOAD")
    print("=" * 60)

    upload_response = requests.post(
        f"{BASE_URL}/api-media-upload",
        headers=headers,
        json={
            "url": video_url
        },
        timeout=120
    )

    print(
        "Media upload status:",
        upload_response.status_code
    )

    if not upload_response.ok:
        raise RuntimeError(
            "Status 200 media upload failed: "
            + upload_response.text
        )

    upload_data = upload_response.json()

    file_id = (
        upload_data.get("file_id")
        or upload_data.get("mediaID")
        or upload_data.get("mediaId")
    )

    if not file_id:
        raise RuntimeError(
            "Status 200 did not return a file ID: "
            + str(upload_data)
        )

    print(
        "Status 200 media ID:",
        file_id
    )

    # -----------------------------
    # STEP 2: Publish to TikTok
    # -----------------------------

    print("=" * 60)
    print("STATUS 200 TIKTOK PUBLISH")
    print("=" * 60)

    publish_response = requests.post(
        f"{BASE_URL}/post",
        headers=headers,
        json={
            "post": {
                "post": caption,
                "platforms": [
                    {
                        "platform": "tiktok",
                        "accountId": TIKTOK_ACCOUNT,
                        "mediaUrls": [file_id],
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                    }
                ]
            }
        },
        timeout=120
    )

    print(
        "TikTok publish status:",
        publish_response.status_code
    )

    if not publish_response.ok:
        raise RuntimeError(
            "Status 200 TikTok publish failed: "
            + publish_response.text
        )

    result = publish_response.json()

    print("=" * 60)
    print("TIKTOK PUBLISH SUCCESS")
    print("=" * 60)

    print(result)

    return result
