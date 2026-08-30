import os
import requests


# ============================================================
# PROMPTPROHUB — STATUS 200 TIKTOK PUBLISHER
# ============================================================
#
# THIS FILE HANDLES TIKTOK ONLY.
#
# Instagram → remains on Zernio
# YouTube    → remains on Zernio
# TikTok     → Status 200
#
# IMPORTANT:
# The function name MUST remain:
#
#     publish_to_status200()
#
# because the existing bot.py imports that name.
# ============================================================


# ============================================================
# STATUS 200 API
# ============================================================

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
)


# ============================================================
# STATUS 200 TIKTOK CREDENTIALS
# ============================================================
#
# Primary variables:
#
# STATUS200_API_KEY_1
# STATUS200_ACCOUNT_1
#
# These are the variables you configured in Railway.
#
# We also support the older variable names as fallback so
# the bot does not break if an old variable still exists.
# ============================================================


STATUS200_API_KEY = os.getenv(
    "STATUS200_API_KEY_1"
)

if not STATUS200_API_KEY:

    STATUS200_API_KEY = os.getenv(
        "STATUS200_API_KEY"
    )


STATUS200_ACCOUNT = os.getenv(
    "STATUS200_ACCOUNT_1"
)

if not STATUS200_ACCOUNT:

    STATUS200_ACCOUNT = os.getenv(
        "STATUS200_TIKTOK_ACCOUNT"
    )


# ============================================================
# PLATFORM
# ============================================================

STATUS200_PLATFORM = "tiktok"


# ============================================================
# RAILWAY PUBLIC DOMAIN
# ============================================================

RAILWAY_PUBLIC_DOMAIN = os.getenv(
    "RAILWAY_PUBLIC_DOMAIN"
)

RAILWAY_PUBLIC_URL = os.getenv(
    "RAILWAY_PUBLIC_URL"
)


# ============================================================
# GET RAILWAY PUBLIC URL
# ============================================================

def get_railway_public_url():

    # --------------------------------------------------------
    # Preferred Railway variable
    # --------------------------------------------------------

    if RAILWAY_PUBLIC_DOMAIN:

        domain = RAILWAY_PUBLIC_DOMAIN.strip()

        if not domain.startswith(
            ("http://", "https://")
        ):

            domain = (
                "https://"
                + domain
            )

        return domain.rstrip("/")


    # --------------------------------------------------------
    # Compatibility with old variable
    # --------------------------------------------------------

    if RAILWAY_PUBLIC_URL:

        url = RAILWAY_PUBLIC_URL.strip()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = (
                "https://"
                + url
            )

        return url.rstrip("/")


    raise RuntimeError(
        "Railway public URL is missing. "
        "Configure RAILWAY_PUBLIC_DOMAIN "
        "or RAILWAY_PUBLIC_URL."
    )


# ============================================================
# BUILD PUBLIC VIDEO URL
# ============================================================

def get_public_video_url(video_path):

    if not video_path:

        raise ValueError(
            "No video path was provided."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    filename = os.path.basename(
        video_path
    )


    base_url = get_railway_public_url()


    return (
        f"{base_url}/videos/{filename}"
    )


# ============================================================
# STATUS 200 HEADERS
# ============================================================

def get_headers():

    if not STATUS200_API_KEY:

        raise RuntimeError(
            "STATUS200_API_KEY_1 is not configured "
            "in Railway Variables."
        )


    return {

        "Authorization":
            f"Bearer {STATUS200_API_KEY}",

        "Content-Type":
            "application/json",

        "Accept":
            "application/json"

    }


# ============================================================
# PUBLISH TO STATUS 200 → TIKTOK
# ============================================================

def publish_to_status200(
    video_path,
    caption
):

    """
    Publish one generated video to TikTok through Status 200.

    Instagram and YouTube are NOT touched by this file.

    Flow:

        Generated video
              ↓
        Railway public URL
              ↓
        Status 200 media upload
              ↓
        media/file ID
              ↓
        Status 200 TikTok post
              ↓
        Connected TikTok account
    """

    print()
    print("=" * 60)
    print(
        "PROMPTPROHUB STATUS 200 → TIKTOK"
    )
    print("=" * 60)


    # ========================================================
    # CONFIGURATION CHECK
    # ========================================================

    if not STATUS200_API_KEY:

        raise RuntimeError(
            "STATUS200_API_KEY_1 is missing "
            "from Railway Variables."
        )


    if not STATUS200_ACCOUNT:

        raise RuntimeError(
            "STATUS200_ACCOUNT_1 is missing "
            "from Railway Variables."
        )


    # ========================================================
    # VIDEO CHECK
    # ========================================================

    if not video_path:

        raise ValueError(
            "No video path provided."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video file does not exist: {video_path}"
        )


    # ========================================================
    # PUBLIC VIDEO URL
    # ========================================================

    video_url = get_public_video_url(
        video_path
    )


    # ========================================================
    # DEBUG
    # ========================================================

    print(
        "Platform:",
        STATUS200_PLATFORM
    )

    print(
        "Status 200 account:",
        STATUS200_ACCOUNT
    )

    print(
        "Local video:",
        video_path
    )

    print(
        "Public video URL:",
        video_url
    )


    # ========================================================
    # HEADERS
    # ========================================================

    headers = get_headers()


    # ========================================================
    # STEP 1
    # UPLOAD MEDIA TO STATUS 200
    # ========================================================

    print()
    print("-" * 60)
    print(
        "STEP 1 — STATUS 200 MEDIA UPLOAD"
    )
    print("-" * 60)


    upload_url = (
        f"{STATUS200_BASE_URL}"
        "/api-media-upload"
    )


    upload_payload = {

        "url":
            video_url

    }


    print(
        "Status 200 media endpoint:",
        upload_url
    )


    upload_response = requests.post(

        upload_url,

        headers=headers,

        json=upload_payload,

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

    except Exception as e:

        raise RuntimeError(

            "Status 200 returned invalid "
            f"media-upload JSON: {e}"

        )


    # ========================================================
    # GET MEDIA ID
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

        or upload_data.get(
            "id"
        )

    )


    if not file_id:

        raise RuntimeError(

            "Status 200 media upload succeeded "
            "but no media/file ID was returned.\n"
            f"Response: {upload_data}"

        )


    print(
        "Status 200 media ID:",
        file_id
    )


    # ========================================================
    # STEP 2
    # CREATE TIKTOK POST
    # ========================================================

    print()
    print("-" * 60)
    print(
        "STEP 2 — STATUS 200 → TIKTOK"
    )
    print("-" * 60)


    # --------------------------------------------------------
    # TikTok post data
    # --------------------------------------------------------

    post_data = {

        "accountId":
            STATUS200_ACCOUNT,

        "platform":
            "tiktok",

        "content": {

            "text":
                str(caption or "").strip(),

            "mediaID": [

                file_id

            ]

        },

        "tiktok": {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }

    }


    publish_payload = {

        "post":
            post_data

    }


    print(
        "TikTok account:",
        STATUS200_ACCOUNT
    )

    print(
        "TikTok media ID:",
        file_id
    )

    print(
        "TikTok privacy:",
        "PUBLIC_TO_EVERYONE"
    )


    # ========================================================
    # STEP 3
    # SEND POST TO STATUS 200
    # ========================================================

    publish_url = (
        f"{STATUS200_BASE_URL}"
        "/api-posts"
    )


    print(
        "Status 200 post endpoint:",
        publish_url
    )


    publish_response = requests.post(

        publish_url,

        headers=headers,

        json=publish_payload,

        timeout=120

    )


    print(
        "TikTok publish HTTP status:",
        publish_response.status_code
    )


    print(
        "TikTok publish response:",
        publish_response.text
    )


    # ========================================================
    # CHECK PUBLISH RESULT
    # ========================================================

    if not publish_response.ok:

        raise RuntimeError(

            "Status 200 TikTok publishing failed: "
            + publish_response.text

        )


    # ========================================================
    # PARSE RESULT
    # ========================================================

    try:

        result = (
            publish_response.json()
        )

    except Exception as e:

        raise RuntimeError(

            "Status 200 returned invalid "
            f"TikTok publish JSON: {e}"

        )


    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("=" * 60)
    print(
        "STATUS 200 → TIKTOK SUCCESS"
    )
    print("=" * 60)

    print(
        "Account:",
        STATUS200_ACCOUNT
    )

    print(
        "Platform:",
        "TikTok"
    )

    print(
        "Result:",
        result
    )

    print("=" * 60)


    return result


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================
#
# In case another part of the project uses this name.
# ============================================================

def publish_to_tiktok(
    video_path,
    caption
):

    return publish_to_status200(
        video_path,
        caption
    )


# ============================================================
# CONFIGURATION TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print(
        "PROMPTPROHUB STATUS 200 TIKTOK CONFIGURATION"
    )
    print("=" * 60)


    print(
        "STATUS200_API_KEY_1:",
        "SET"
        if STATUS200_API_KEY
        else "MISSING"
    )


    print(
        "STATUS200_ACCOUNT_1:",
        STATUS200_ACCOUNT
        if STATUS200_ACCOUNT
        else "MISSING"
    )


    print(
        "RAILWAY_PUBLIC_DOMAIN:",
        RAILWAY_PUBLIC_DOMAIN
        if RAILWAY_PUBLIC_DOMAIN
        else "MISSING"
    )


    print(
        "RAILWAY_PUBLIC_URL:",
        RAILWAY_PUBLIC_URL
        if RAILWAY_PUBLIC_URL
        else "MISSING"
    )


    print("=" * 60)
