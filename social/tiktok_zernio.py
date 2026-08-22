import os
import uuid
import requests


# ============================================================
# TIKTOK ZERNIO UPLOADER
# PromptProHub AI Content Factory
# ============================================================

ZERNIO_API_KEY = os.getenv(
    "ZERNIO_TIKTOK_API_KEY"
)

ZERNIO_TIKTOK_ACCOUNT_ID = os.getenv(
    "ZERNIO_TIKTOK_ACCOUNT_ID"
)

ZERNIO_BASE_URL = (
    "https://zernio.com/api/v1"
)


# ============================================================
# RAILWAY PUBLIC URL
# ============================================================

RAILWAY_PUBLIC_DOMAIN = os.getenv(
    "RAILWAY_PUBLIC_DOMAIN"
)

RAILWAY_PUBLIC_URL = os.getenv(
    "RAILWAY_PUBLIC_URL"
)


# ============================================================
# VALIDATE
# ============================================================

def validate_config():

    if not ZERNIO_API_KEY:
        raise RuntimeError(
            "ZERNIO_TIKTOK_API_KEY is missing "
            "from Railway Variables."
        )

    if not ZERNIO_TIKTOK_ACCOUNT_ID:
        raise RuntimeError(
            "ZERNIO_TIKTOK_ACCOUNT_ID is missing "
            "from Railway Variables."
        )


# ============================================================
# RAILWAY URL
# ============================================================

def get_railway_public_url():

    if RAILWAY_PUBLIC_DOMAIN:

        url = RAILWAY_PUBLIC_DOMAIN.strip()

        if not url.startswith(
            ("http://", "https://")
        ):
            url = "https://" + url

        return url.rstrip("/")


    if RAILWAY_PUBLIC_URL:

        url = RAILWAY_PUBLIC_URL.strip()

        if not url.startswith(
            ("http://", "https://")
        ):
            url = "https://" + url

        return url.rstrip("/")


    raise RuntimeError(
        "RAILWAY_PUBLIC_DOMAIN or "
        "RAILWAY_PUBLIC_URL is missing."
    )


# ============================================================
# PUBLIC VIDEO URL
# ============================================================

def get_public_video_url(video_path):

    if not video_path:
        raise ValueError(
            "No video path supplied."
        )

    filename = os.path.basename(
        video_path
    )

    return (
        f"{get_railway_public_url()}"
        f"/videos/{filename}"
    )


# ============================================================
# PUBLISH TIKTOK
# ============================================================

def publish_tiktok(
    video_path,
    caption
):

    validate_config()

    public_video_url = (
        get_public_video_url(
            video_path
        )
    )

    print("=" * 60)
    print("TIKTOK ZERNIO PUBLISHER")
    print("=" * 60)

    print(
        "TikTok Account:",
        ZERNIO_TIKTOK_ACCOUNT_ID
    )

    print(
        "Video URL:",
        public_video_url
    )

    # --------------------------------------------------------
    # Verify Railway video
    # --------------------------------------------------------

    check = requests.head(
        public_video_url,
        allow_redirects=True,
        timeout=30
    )

    print(
        "Railway HTTP STATUS:",
        check.status_code
    )

    if check.status_code != 200:

        raise RuntimeError(
            "Public video URL is not accessible. "
            f"HTTP {check.status_code}"
        )

    # --------------------------------------------------------
    # Zernio endpoint
    # --------------------------------------------------------

    url = (
        f"{ZERNIO_BASE_URL}/posts"
    )

    request_id = str(
        uuid.uuid4()
    )

    headers = {

        "Authorization":
            f"Bearer {ZERNIO_API_KEY}",

        "Accept":
            "application/json",

        "Content-Type":
            "application/json",

        "x-request-id":
            request_id
    }

    # --------------------------------------------------------
    # TikTok payload
    # --------------------------------------------------------

    payload = {

        "content":
            caption or "",

        "mediaItems": [

            {
                "type":
                    "video",

                "url":
                    public_video_url
            }

        ],

        "platforms": [

            {
                "platform":
                    "tiktok",

                "accountId":
                    ZERNIO_TIKTOK_ACCOUNT_ID
            }

        ],

        "tiktokSettings": {

            "privacy_level":
                "PUBLIC_TO_EVERYONE",

            "allow_comment":
                True,

            "allow_duet":
                True,

            "allow_stitch":
                True,

            "content_preview_confirmed":
                True,

            "express_consent_given":
                True
        },

        "publishNow":
            True
    }

    print(
        "Publishing TikTok..."
    )

    try:

        response = requests.post(

            url,

            headers=headers,

            json=payload,

            timeout=300
        )

    except requests.RequestException as e:

        raise RuntimeError(
            f"TikTok Zernio request failed: {e}"
        )

    print(
        "ZERNIO HTTP STATUS:",
        response.status_code
    )

    print(
        "ZERNIO RESPONSE:",
        response.text
    )

    try:

        result = response.json()

    except ValueError:

        raise RuntimeError(
            "Zernio returned invalid JSON:\n"
            + response.text
        )

    if response.status_code not in (
        200,
        201
    ):

        raise RuntimeError(
            "Zernio TikTok publishing failed:\n"
            + str(result)
        )

    print("=" * 60)
    print("TIKTOK PUBLISHED SUCCESSFULLY")
    print("=" * 60)

    return result


# ============================================================
# COMPATIBILITY
# ============================================================

def publish_to_tiktok(
    video_path,
    caption
):

    return publish_tiktok(
        video_path,
        caption
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    try:

        validate_config()

        print(
            "TikTok Zernio configuration is valid."
        )

        print(
            "Account:",
            ZERNIO_TIKTOK_ACCOUNT_ID
        )

    except Exception as e:

        print(
            "CONFIGURATION ERROR:",
            e
        )
