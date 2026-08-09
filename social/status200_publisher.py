import os
import requests


STATUS200_API_KEY = os.getenv("STATUS200_API_KEY")

TIKTOK_ACCOUNT = os.getenv(
    "STATUS200_TIKTOK_ACCOUNT",
    "@Promptprohub"
)

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
)

RAILWAY_PUBLIC_URL = os.getenv(
    "RAILWAY_PUBLIC_URL"
)


def publish_to_status200(video_path, caption):
    """
    Send a locally generated PromptProHub video
    to Status 200.

    Status 200 then publishes the video to the
    connected social account.
    """

    print("=" * 60)
    print("STATUS 200 PUBLISHER")
    print("=" * 60)

    # -------------------------------------------------
    # CHECK API KEY
    # -------------------------------------------------

    if not STATUS200_API_KEY:

        raise RuntimeError(
            "STATUS200_API_KEY is not configured "
            "in Railway Variables."
        )

    # -------------------------------------------------
    # CHECK VIDEO
    # -------------------------------------------------

    if not video_path:

        raise ValueError(
            "No video path provided."
        )

    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )

    # -------------------------------------------------
    # CHECK PUBLIC RAILWAY URL
    # -------------------------------------------------

    if not RAILWAY_PUBLIC_URL:

        raise RuntimeError(
            "RAILWAY_PUBLIC_URL is not configured "
            "in Railway Variables."
        )

    # Remove trailing slash
    base_url = RAILWAY_PUBLIC_URL.rstrip("/")

    # -------------------------------------------------
    # CREATE PUBLIC VIDEO URL
    # -------------------------------------------------

    filename = os.path.basename(
        video_path
    )

    video_url = (
        f"{base_url}/videos/{filename}"
    )

    print(
        "Local video:",
        video_path
    )

    print(
        "Public video URL:",
        video_url
    )

    print(
        "Status 200 account:",
        TIKTOK_ACCOUNT
    )

    # -------------------------------------------------
    # HEADERS
    # -------------------------------------------------

    headers = {
        "Authorization":
            f"Bearer {STATUS200_API_KEY}",

        "Content-Type":
            "application/json",
    }

    # =================================================
    # STEP 1 — SEND VIDEO TO STATUS 200
    # =================================================

    print("=" * 60)
    print("STATUS 200 MEDIA UPLOAD")
    print("=" * 60)

    upload_response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-media-upload",

        headers=headers,

        json={
            "url": video_url
        },

        timeout=120
    )

    print(
        "Media upload HTTP status:",
        upload_response.status_code
    )

    print(
        "Media upload response:",
        upload_response.text
    )

    if not upload_response.ok:

        raise RuntimeError(
            "Status 200 media upload failed: "
            + upload_response.text
        )

    try:

        upload_data = (
            upload_response.json()
        )

    except Exception:

        raise RuntimeError(
            "Status 200 returned an invalid "
            "media upload response."
        )

    # -------------------------------------------------
    # GET MEDIA ID
    # -------------------------------------------------

    file_id = (

        upload_data.get("file_id")

        or upload_data.get("mediaID")

        or upload_data.get("mediaId")

    )

    if not file_id:

        raise RuntimeError(
            "Status 200 did not return a "
            f"media/file ID: {upload_data}"
        )

    print(
        "Status 200 media ID:",
        file_id
    )

    # =================================================
    # STEP 2 — ASK STATUS 200 TO PUBLISH
    # =================================================

    print("=" * 60)
    print("STATUS 200 → CONNECTED SOCIAL ACCOUNT")
    print("=" * 60)

    publish_response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-posts",

        headers=headers,

        json={
            "post": {

                "accountId":
                    TIKTOK_ACCOUNT,

                "platform":
                    "tiktok",

                "content": {

                    "text":
                        caption,

                    "mediaID": [
                        file_id
                    ]

                },

                "tiktok": {

                    "privacyLevel":
                        "PUBLIC_TO_EVERYONE"

                }

            }
        },

        timeout=120
    )

    print(
        "Status 200 publish HTTP status:",
        publish_response.status_code
    )

    print(
        "Status 200 publish response:",
        publish_response.text
    )

    if not publish_response.ok:

        raise RuntimeError(
            "Status 200 publish failed: "
            + publish_response.text
        )

    try:

        result = (
            publish_response.json()
        )

    except Exception:

        raise RuntimeError(
            "Status 200 returned an invalid "
            "publish response."
        )

    print("=" * 60)
    print("STATUS 200 PUBLISH REQUEST SUCCESSFUL")
    print("=" * 60)

    print(result)

    return result
