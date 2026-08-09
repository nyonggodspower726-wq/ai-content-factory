# ============================================================
# INSTAGRAM ZERNIO UPLOADER
# PromptProHub AI Content Factory
#
# IMPORTANT:
# This version DOES NOT use Zernio's direct media upload.
#
# Flow:
#
# AI VIDEO
#    ↓
# Railway public /videos/ URL
#    ↓
# Zernio Posts API
#    ↓
# Instagram Reels
#
# This avoids Zernio HTTP 413:
# "Request Entity Too Large"
# ============================================================

import os
import uuid
import requests


# ============================================================
# CONFIGURATION
# ============================================================

ZERNIO_API_KEY = os.getenv(
    "ZERNIO_API_KEY"
)

ZERNIO_INSTAGRAM_ACCOUNT_ID = os.getenv(
    "ZERNIO_INSTAGRAM_ACCOUNT_ID"
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
# VALIDATE CONFIGURATION
# ============================================================

def validate_config():

    if not ZERNIO_API_KEY:

        raise RuntimeError(
            "ZERNIO_API_KEY is missing "
            "from Railway Variables."
        )


    if not ZERNIO_INSTAGRAM_ACCOUNT_ID:

        raise RuntimeError(
            "ZERNIO_INSTAGRAM_ACCOUNT_ID "
            "is missing from Railway Variables."
        )


# ============================================================
# GET RAILWAY BASE URL
# ============================================================

def get_railway_public_url():

    # --------------------------------------------------------
    # OPTION 1
    # --------------------------------------------------------

    if RAILWAY_PUBLIC_DOMAIN:

        base_url = (
            RAILWAY_PUBLIC_DOMAIN.strip()
        )

        if not base_url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            base_url = (
                "https://"
                + base_url
            )

        return base_url.rstrip("/")


    # --------------------------------------------------------
    # OPTION 2
    # --------------------------------------------------------

    if RAILWAY_PUBLIC_URL:

        base_url = (
            RAILWAY_PUBLIC_URL.strip()
        )

        if not base_url.startswith(
            (
                "http://",
                "https://"
            )
        ):

            base_url = (
                "https://"
                + base_url
            )

        return base_url.rstrip("/")


    # --------------------------------------------------------
    # NOTHING FOUND
    # --------------------------------------------------------

    raise RuntimeError(
        "Railway public URL is not configured. "
        "Set RAILWAY_PUBLIC_DOMAIN or "
        "RAILWAY_PUBLIC_URL in Railway Variables."
    )


# ============================================================
# BUILD PUBLIC VIDEO URL
# ============================================================

def get_public_video_url(
    video_path
):

    if not video_path:

        raise ValueError(
            "No video path was supplied."
        )


    filename = os.path.basename(
        video_path
    )


    if not filename:

        raise ValueError(
            "Could not determine video filename."
        )


    base_url = (
        get_railway_public_url()
    )


    public_url = (
        f"{base_url}/videos/{filename}"
    )


    return public_url


# ============================================================
# HEADERS
# ============================================================

def get_headers():

    return {

        "Authorization":
            f"Bearer {ZERNIO_API_KEY}",

        "Accept":
            "application/json",

        "Content-Type":
            "application/json"

    }


# ============================================================
# CHECK PUBLIC VIDEO
# ============================================================
#
# We perform a HEAD request first.
#
# This helps detect:
#
# - wrong Railway URL
# - missing video
# - inaccessible video
#
# before sending the post to Zernio.
#
# ============================================================

def check_public_video(
    public_video_url
):

    print()
    print("=" * 60)
    print("CHECKING PUBLIC VIDEO URL")
    print("=" * 60)

    print(
        "URL:",
        public_video_url
    )


    try:

        response = requests.head(

            public_video_url,

            allow_redirects=True,

            timeout=30

        )

    except requests.RequestException as e:

        raise RuntimeError(
            "Could not reach the Railway "
            f"video URL: {e}"
        )


    print(
        "HTTP STATUS:",
        response.status_code
    )


    content_type = (
        response.headers.get(
            "Content-Type",
            ""
        )
    )


    content_length = (
        response.headers.get(
            "Content-Length"
        )
    )


    print(
        "Content-Type:",
        content_type
    )


    print(
        "Content-Length:",
        content_length
    )


    # --------------------------------------------------------
    # ACCEPT 200
    # --------------------------------------------------------

    if response.status_code != 200:

        raise RuntimeError(
            "Railway video URL is not publicly "
            "accessible. HTTP status: "
            f"{response.status_code}\n"
            f"URL: {public_video_url}"
        )


    # --------------------------------------------------------
    # CONTENT TYPE WARNING
    # --------------------------------------------------------

    if content_type:

        if (
            "video" not in
            content_type.lower()
            and
            "octet-stream" not in
            content_type.lower()
        ):

            print(
                "WARNING: Railway returned "
                f"Content-Type: {content_type}"
            )


    print(
        "Public video URL is reachable."
    )


    print("=" * 60)


    return True


# ============================================================
# CREATE INSTAGRAM REEL
# ============================================================

def publish_instagram_reel(
    video_path,
    caption
):

    validate_config()


    if not caption:

        caption = ""


    # ========================================================
    # STEP 1 — MAKE PUBLIC RAILWAY URL
    # ========================================================

    public_video_url = (
        get_public_video_url(
            video_path
        )
    )


    print()
    print("=" * 60)
    print("INSTAGRAM ZERNIO PUBLISHER")
    print("=" * 60)


    print(
        "Instagram Account:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
    )


    print(
        "Local Video:",
        video_path
    )


    print(
        "Public Video URL:",
        public_video_url
    )


    print(
        "Caption:",
        caption
    )


    # ========================================================
    # STEP 2 — VERIFY RAILWAY URL
    # ========================================================

    check_public_video(
        public_video_url
    )


    # ========================================================
    # STEP 3 — CREATE ZERNIO POST
    # ========================================================

    url = (
        f"{ZERNIO_BASE_URL}"
        "/posts"
    )


    request_id = str(
        uuid.uuid4()
    )


    headers = get_headers()

    headers.update({

        "x-request-id":
            request_id

    })


    # ========================================================
    # ZERNIO PAYLOAD
    # ========================================================
    #
    # IMPORTANT:
    #
    # There is NO:
    #
    # /media/upload-direct
    #
    # request anymore.
    #
    # Zernio receives the Railway public video URL
    # directly as the media URL.
    #
    # ========================================================

    payload = {

        "content":
            caption,

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
                    "instagram",

                "accountId":
                    ZERNIO_INSTAGRAM_ACCOUNT_ID,

                "platformSpecificData": {

                    "contentType":
                        "reels",

                    "shareToFeed":
                        True,

                    "isAiGenerated":
                        True

                }

            }

        ],

        "publishNow":
            True

    }


    # ========================================================
    # DEBUG
    # ========================================================

    print()
    print("=" * 60)
    print("ZERNIO INSTAGRAM REQUEST")
    print("=" * 60)


    print(
        "Endpoint:",
        url
    )


    print(
        "Request ID:",
        request_id
    )


    print(
        "Instagram Account:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
    )


    print(
        "Media URL:",
        public_video_url
    )


    print(
        "Publishing Instagram Reel..."
    )


    # ========================================================
    # STEP 4 — SEND TO ZERNIO
    # ========================================================

    try:

        response = requests.post(

            url,

            headers=headers,

            json=payload,

            timeout=300

        )

    except requests.RequestException as e:

        raise RuntimeError(
            "Zernio Instagram publishing "
            f"request failed: {e}"
        )


    # ========================================================
    # RESPONSE
    # ========================================================

    print()
    print(
        "ZERNIO HTTP STATUS:",
        response.status_code
    )


    print(
        "ZERNIO RESPONSE:"
    )


    print(
        response.text
    )


    # ========================================================
    # PARSE JSON
    # ========================================================

    try:

        result = (
            response.json()
        )

    except ValueError:

        raise RuntimeError(
            "Zernio returned invalid JSON:\n"
            + response.text
        )


    # ========================================================
    # ERROR
    # ========================================================

    if response.status_code not in (
        200,
        201
    ):

        raise RuntimeError(
            "Zernio Instagram publishing "
            "failed:\n"
            + str(result)
        )


    # ========================================================
    # POST INFORMATION
    # ========================================================

    post = result.get(
        "post",
        {}
    )


    post_id = post.get(
        "_id"
    )


    # ========================================================
    # PLATFORM URL
    # ========================================================

    platform_url = None


    platforms = post.get(
        "platforms",
        []
    )


    if isinstance(
        platforms,
        list
    ):

        for platform in platforms:

            if not isinstance(
                platform,
                dict
            ):

                continue


            if (
                platform.get(
                    "platform"
                )
                == "instagram"
            ):

                platform_url = (
                    platform.get(
                        "platformPostUrl"
                    )
                )

                break


    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("=" * 60)
    print(
        "INSTAGRAM REEL PUBLISHED SUCCESSFULLY"
    )
    print("=" * 60)


    if post_id:

        print(
            "Zernio Post ID:",
            post_id
        )


    if platform_url:

        print(
            "Instagram URL:",
            platform_url
        )

    else:

        print(
            "Instagram URL: "
            "Not returned by Zernio yet."
        )


    print("=" * 60)


    return result


# ============================================================
# COMPATIBILITY FUNCTION
# ============================================================
#
# bot.py already calls:
#
# publish_to_instagram(video, caption)
#
# Therefore we keep this function name unchanged.
#
# ============================================================

def publish_to_instagram(
    video_path,
    caption
):

    return publish_instagram_reel(
        video_path,
        caption
    )


# ============================================================
# TEST MODE
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("INSTAGRAM ZERNIO UPLOADER TEST")
    print("=" * 60)


    try:

        validate_config()


        print(
            "ZERNIO_API_KEY: configured"
        )


        print(
            "INSTAGRAM ACCOUNT ID:",
            ZERNIO_INSTAGRAM_ACCOUNT_ID
        )


        railway_url = (
            get_railway_public_url()
        )


        print(
            "Railway Public URL:",
            railway_url
        )


        print()
        print(
            "Instagram Zernio uploader "
            "configuration is valid."
        )


    except Exception as e:

        print()
        print(
            "CONFIGURATION ERROR:"
        )

        print(
            str(e)
        )


    print("=" * 60)
