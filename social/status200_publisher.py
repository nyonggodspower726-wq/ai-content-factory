import os
import requests


# ============================================================
# STATUS 200 CONFIGURATION
# ============================================================

STATUS200_API_KEY = os.getenv(
    "STATUS200_API_KEY"
)

STATUS200_ACCOUNT = os.getenv(
    "STATUS200_TIKTOK_ACCOUNT",
    "@Promptprohub"
)

STATUS200_PLATFORM = os.getenv(
    "STATUS200_PLATFORM",
    "tiktok"
)

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
)


# ============================================================
# RAILWAY PUBLIC DOMAIN
# ============================================================

# Railway provides RAILWAY_PUBLIC_DOMAIN automatically
# when the service has a public domain.

RAILWAY_PUBLIC_DOMAIN = os.getenv(
    "RAILWAY_PUBLIC_DOMAIN"
)

# Keep compatibility with the old variable in case it exists.
RAILWAY_PUBLIC_URL = os.getenv(
    "RAILWAY_PUBLIC_URL"
)


# ============================================================
# BUILD PUBLIC RAILWAY URL
# ============================================================

def get_railway_public_url():

    # Prefer Railway's official public-domain variable.
    if RAILWAY_PUBLIC_DOMAIN:

        domain = RAILWAY_PUBLIC_DOMAIN.strip()

        if not domain.startswith("http://") and \
           not domain.startswith("https://"):

            domain = "https://" + domain

        return domain.rstrip("/")

    # Fallback to manually configured URL.
    if RAILWAY_PUBLIC_URL:

        url = RAILWAY_PUBLIC_URL.strip()

        if not url.startswith("http://") and \
           not url.startswith("https://"):

            url = "https://" + url

        return url.rstrip("/")

    raise RuntimeError(
        "Railway public domain is not available. "
        "RAILWAY_PUBLIC_DOMAIN was not found."
    )


# ============================================================
# PUBLISH TO STATUS 200
# ============================================================

def publish_to_status200(video_path, caption):

    """
    Send a locally generated PromptProHub video
    to Status 200.

    Flow:

        Local video
            ↓
        Railway public URL
            ↓
        Status 200 media upload
            ↓
        Status 200 file_id
            ↓
        Status 200 publish
            ↓
        Connected social account
    """

    print("=" * 60)
    print("STATUS 200 PUBLISHER")
    print("=" * 60)


    # ========================================================
    # CHECK API KEY
    # ========================================================

    if not STATUS200_API_KEY:

        raise RuntimeError(
            "STATUS200_API_KEY is not configured "
            "in Railway Variables."
        )


    # ========================================================
    # CHECK VIDEO PATH
    # ========================================================

    if not video_path:

        raise ValueError(
            "No video path provided."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    # ========================================================
    # GET PUBLIC RAILWAY URL
    # ========================================================

    base_url = get_railway_public_url()


    # ========================================================
    # CREATE PUBLIC VIDEO URL
    # ========================================================

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
        "Railway public domain:",
        base_url
    )

    print(
        "Public video URL:",
        video_url
    )

    print(
        "Status 200 account:",
        STATUS200_ACCOUNT
    )

    print(
        "Status 200 platform:",
        STATUS200_PLATFORM
    )


    # ========================================================
    # HEADERS
    # ========================================================

    headers = {

        "Authorization":
            f"Bearer {STATUS200_API_KEY}",

        "Content-Type":
            "application/json",

    }


    # ========================================================
    # STEP 1
    # STATUS 200 MEDIA UPLOAD
    # ========================================================

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


    # ========================================================
    # PARSE MEDIA RESPONSE
    # ========================================================

    try:

        upload_data = (
            upload_response.json()
        )

    except Exception:

        raise RuntimeError(

            "Status 200 returned an invalid "
            "media upload response."

        )


    # ========================================================
    # GET FILE ID
    # ========================================================

    file_id = (

        upload_data.get(
            "file_id"
        )

        or upload_data.get(
            "mediaID"
        )

        or upload_data.get(
            "mediaId"
        )

    )


    if not file_id:

        raise RuntimeError(

            "Status 200 did not return "
            f"a media/file ID: {upload_data}"

        )


    print(
        "Status 200 media ID:",
        file_id
    )


    # ========================================================
    # STEP 2
    # ASK STATUS 200 TO PUBLISH
    # ========================================================

    print("=" * 60)
    print("STATUS 200 → SOCIAL PLATFORM")
    print("=" * 60)


    publish_payload = {

        "post": {

            "accountId":
                STATUS200_ACCOUNT,

            "platform":
                STATUS200_PLATFORM,

            "content": {

                "text":
                    caption,

                "mediaID": [

                    file_id

                ]

            }

        }

    }


    # ========================================================
    # TIKTOK OPTIONS
    # ========================================================

    if STATUS200_PLATFORM.lower() == "tiktok":

        publish_payload["post"]["tiktok"] = {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }


    print(
        "Publishing to:",
        STATUS200_ACCOUNT
    )

    print(
        "Platform:",
        STATUS200_PLATFORM
    )


    # ========================================================
    # SEND PUBLISH REQUEST
    # ========================================================

    publish_response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-posts",

        headers=headers,

        json=publish_payload,

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


    # ========================================================
    # PARSE PUBLISH RESPONSE
    # ========================================================

    try:

        result = (
            publish_response.json()
        )

    except Exception:

        raise RuntimeError(

            "Status 200 returned an invalid "
            "publish response."

        )


    # ========================================================
    # SUCCESS
    # ========================================================

    print("=" * 60)
    print("STATUS 200 PUBLISH REQUEST SUCCESSFUL")
    print("=" * 60)

    print(
        "Status 200 result:",
        result
    )

    print("=" * 60)


    return result
