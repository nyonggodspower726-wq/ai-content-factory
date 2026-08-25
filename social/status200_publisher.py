import os
import requests


# ============================================================
# PROMPTPROHUB ZERNIO MULTI-PLATFORM PUBLISHER
#
# One finished video
#       ↓
# Railway public video URL
#       ↓
# Instagram Zernio account
# TikTok Zernio account
# YouTube Zernio account
#
# Each platform uses its own Zernio API key/account.
# ============================================================


ZERNIO_BASE_URL = "https://zernio.com/api/v1"


# ============================================================
# INSTAGRAM
# ============================================================

ZERNIO_INSTAGRAM_API_KEY = os.getenv(
    "ZERNIO_API_KEY"
)

ZERNIO_INSTAGRAM_ACCOUNT_ID = os.getenv(
    "ZERNIO_INSTAGRAM_ACCOUNT_ID"
)


# ============================================================
# TIKTOK
# ============================================================

ZERNIO_TIKTOK_API_KEY = os.getenv(
    "ZERNIO_TIKTOK_API_KEY"
)

ZERNIO_TIKTOK_ACCOUNT_ID = os.getenv(
    "ZERNIO_TIKTOK_ACCOUNT_ID"
)


# ============================================================
# YOUTUBE
# ============================================================

ZERNIO_YOUTUBE_API_KEY = os.getenv(
    "ZERNIO_YOUTUBE_API_KEY"
)

ZERNIO_YOUTUBE_ACCOUNT_ID = os.getenv(
    "ZERNIO_YOUTUBE_ACCOUNT_ID"
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
# RAILWAY URL
# ============================================================

def get_railway_public_url():

    if RAILWAY_PUBLIC_DOMAIN:

        domain = RAILWAY_PUBLIC_DOMAIN.strip()

        if not domain.startswith(
            ("http://", "https://")
        ):

            domain = "https://" + domain

        return domain.rstrip("/")


    if RAILWAY_PUBLIC_URL:

        url = RAILWAY_PUBLIC_URL.strip()

        if not url.startswith(
            ("http://", "https://")
        ):

            url = "https://" + url

        return url.rstrip("/")


    raise RuntimeError(
        "Railway public URL is missing."
    )


# ============================================================
# BUILD PUBLIC VIDEO URL
# ============================================================

def get_public_video_url(video_path):

    if not video_path:

        raise ValueError(
            "No video path provided."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    filename = os.path.basename(
        video_path
    )


    return (
        f"{get_railway_public_url()}/videos/{filename}"
    )


# ============================================================
# HEADERS
# ============================================================

def get_headers(api_key):

    return {

        "Authorization":
            f"Bearer {api_key}",

        "Accept":
            "application/json",

        "Content-Type":
            "application/json"

    }


# ============================================================
# YOUTUBE TITLE
# ============================================================

def make_youtube_title(caption):

    if not caption:

        return "AI Automation Tips"


    title = str(
        caption
    ).split("\n")[0].strip()


    if not title:

        title = "AI Automation Tips"


    if len(title) > 100:

        title = (
            title[:97].rstrip()
            + "..."
        )


    return title


# ============================================================
# INSTAGRAM
# ============================================================

def publish_instagram(
    video_url,
    caption
):

    print()
    print("=" * 60)
    print("ZERNIO → INSTAGRAM")
    print("=" * 60)


    if not ZERNIO_INSTAGRAM_API_KEY:

        raise RuntimeError(
            "ZERNIO_API_KEY is missing."
        )


    if not ZERNIO_INSTAGRAM_ACCOUNT_ID:

        raise RuntimeError(
            "ZERNIO_INSTAGRAM_ACCOUNT_ID is missing."
        )


    payload = {

        "content":
            caption,

        "mediaItems": [

            {
                "type":
                    "video",

                "url":
                    video_url
            }

        ],

        "platforms": [

            {
                "platform":
                    "instagram",

                "accountId":
                    ZERNIO_INSTAGRAM_ACCOUNT_ID,

                "platformSpecificData": {

                    "isAiGenerated":
                        True

                }

            }

        ],

        "publishNow":
            True

    }


    print(
        "Instagram account:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
    )


    response = requests.post(

        f"{ZERNIO_BASE_URL}/posts",

        headers=get_headers(
            ZERNIO_INSTAGRAM_API_KEY
        ),

        json=payload,

        timeout=300

    )


    print(
        "Instagram HTTP:",
        response.status_code
    )

    print(
        "Instagram response:",
        response.text
    )


    if not response.ok:

        raise RuntimeError(
            "Instagram publishing failed: "
            + response.text
        )


    return response.json()


# ============================================================
# TIKTOK
# ============================================================

def publish_tiktok(
    video_url,
    caption
):

    print()
    print("=" * 60)
    print("ZERNIO → TIKTOK")
    print("=" * 60)


    if not ZERNIO_TIKTOK_API_KEY:

        raise RuntimeError(
            "ZERNIO_TIKTOK_API_KEY is missing."
        )


    if not ZERNIO_TIKTOK_ACCOUNT_ID:

        raise RuntimeError(
            "ZERNIO_TIKTOK_ACCOUNT_ID is missing."
        )


    # IMPORTANT:
    #
    # TikTok settings MUST be inside
    # platformSpecificData.tiktokSettings.
    #
    # This is the structure documented by Zernio.
    #

    payload = {

        "content":
            caption,

        "mediaItems": [

            {
                "type":
                    "video",

                "url":
                    video_url
            }

        ],

        "platforms": [

            {

                "platform":
                    "tiktok",

                "accountId":
                    ZERNIO_TIKTOK_ACCOUNT_ID,

                "platformSpecificData": {

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
                            True,

                        "video_made_with_ai":
                            True

                    }

                }

            }

        ],

        "publishNow":
            True

    }


    print(
        "TikTok account:",
        ZERNIO_TIKTOK_ACCOUNT_ID
    )

    print(
        "Publishing TikTok video..."
    )


    response = requests.post(

        f"{ZERNIO_BASE_URL}/posts",

        headers=get_headers(
            ZERNIO_TIKTOK_API_KEY
        ),

        json=payload,

        timeout=300

    )


    print(
        "TikTok HTTP:",
        response.status_code
    )

    print(
        "TikTok response:",
        response.text
    )


    if not response.ok:

        raise RuntimeError(
            "TikTok publishing failed: "
            + response.text
        )


    return response.json()


# ============================================================
# YOUTUBE
# ============================================================

def publish_youtube(
    video_url,
    caption
):

    print()
    print("=" * 60)
    print("ZERNIO → YOUTUBE")
    print("=" * 60)


    if not ZERNIO_YOUTUBE_API_KEY:

        raise RuntimeError(
            "ZERNIO_YOUTUBE_API_KEY is missing."
        )


    if not ZERNIO_YOUTUBE_ACCOUNT_ID:

        raise RuntimeError(
            "ZERNIO_YOUTUBE_ACCOUNT_ID is missing."
        )


    title = make_youtube_title(
        caption
    )


    payload = {

        "content":
            caption,

        "mediaItems": [

            {
                "type":
                    "video",

                "url":
                    video_url
            }

        ],

        "platforms": [

            {

                "platform":
                    "youtube",

                "accountId":
                    ZERNIO_YOUTUBE_ACCOUNT_ID,

                "platformSpecificData": {

                    "title":
                        title,

                    "visibility":
                        "public"

                }

            }

        ],

        "publishNow":
            True

    }


    print(
        "YouTube account:",
        ZERNIO_YOUTUBE_ACCOUNT_ID
    )

    print(
        "YouTube title:",
        title
    )

    print(
        "Publishing YouTube video..."
    )


    response = requests.post(

        f"{ZERNIO_BASE_URL}/posts",

        headers=get_headers(
            ZERNIO_YOUTUBE_API_KEY
        ),

        json=payload,

        timeout=300

    )


    print(
        "YouTube HTTP:",
        response.status_code
    )

    print(
        "YouTube response:",
        response.text
    )


    if not response.ok:

        raise RuntimeError(
            "YouTube publishing failed: "
            + response.text
        )


    return response.json()


# ============================================================
# MAIN PUBLISHER
# ============================================================

def publish_to_zernio(
    video_path,
    caption
):

    print()
    print("=" * 60)
    print(
        "PROMPTPROHUB ZERNIO MULTI-PLATFORM PUBLISHER"
    )
    print("=" * 60)


    video_url = get_public_video_url(
        video_path
    )


    print(
        "Video URL:",
        video_url
    )


    successful = []

    failed = []


    # ========================================================
    # INSTAGRAM
    # ========================================================

    try:

        result = publish_instagram(
            video_url,
            caption
        )

        successful.append(
            {
                "platform":
                    "instagram",

                "result":
                    result
            }
        )

        print(
            "INSTAGRAM → SUCCESS"
        )

    except Exception as e:

        failed.append(
            {
                "platform":
                    "instagram",

                "error":
                    str(e)
            }
        )

        print(
            "INSTAGRAM → FAILED:",
            e
        )


    # ========================================================
    # TIKTOK
    # ========================================================

    try:

        result = publish_tiktok(
            video_url,
            caption
        )

        successful.append(
            {
                "platform":
                    "tiktok",

                "result":
                    result
            }
        )

        print(
            "TIKTOK → SUCCESS"
        )

    except Exception as e:

        failed.append(
            {
                "platform":
                    "tiktok",

                "error":
                    str(e)
            }
        )

        print(
            "TIKTOK → FAILED:",
            e
        )


    # ========================================================
    # YOUTUBE
    # ========================================================

    try:

        result = publish_youtube(
            video_url,
            caption
        )

        successful.append(
            {
                "platform":
                    "youtube",

                "result":
                    result
            }
        )

        print(
            "YOUTUBE → SUCCESS"
        )

    except Exception as e:

        failed.append(
            {
                "platform":
                    "youtube",

                "error":
                    str(e)
            }
        )

        print(
            "YOUTUBE → FAILED:",
            e
        )


    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("ZERNIO PUBLISH SUMMARY")
    print("=" * 60)

    print(
        "Successful:",
        len(successful)
    )

    print(
        "Failed:",
        len(failed)
    )


    for item in successful:

        print(
            "SUCCESS:",
            item["platform"]
        )


    for item in failed:

        print(
            "FAILED:",
            item["platform"],
            "→",
            item["error"]
        )


    print("=" * 60)


    return {

        "success":
            len(successful) > 0,

        "total":
            3,

        "successful":
            successful,

        "failed":
            failed

    }


# ============================================================
# COMPATIBILITY
# ============================================================

def publish_to_status200(
    video_path,
    caption
):

    return publish_to_zernio(
        video_path,
        caption
    )


def publish_to_socials(
    video_path,
    caption
):

    return publish_to_zernio(
        video_path,
        caption
    )


# ============================================================
# CONFIGURATION TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("PROMPTPROHUB ZERNIO CONFIGURATION")
    print("=" * 60)

    print(
        "Instagram API:",
        "SET"
        if ZERNIO_INSTAGRAM_API_KEY
        else "MISSING"
    )

    print(
        "Instagram Account:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
        or "MISSING"
    )

    print(
        "TikTok API:",
        "SET"
        if ZERNIO_TIKTOK_API_KEY
        else "MISSING"
    )

    print(
        "TikTok Account:",
        ZERNIO_TIKTOK_ACCOUNT_ID
        or "MISSING"
    )

    print(
        "YouTube API:",
        "SET"
        if ZERNIO_YOUTUBE_API_KEY
        else "MISSING"
    )

    print(
        "YouTube Account:",
        ZERNIO_YOUTUBE_ACCOUNT_ID
        or "MISSING"
    )

    print("=" * 60)
