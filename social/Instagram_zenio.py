# ============================================================
# INSTAGRAM ZERNIO UPLOADER
# PromptProHub AI Content Factory
# ============================================================

import os
import uuid
import mimetypes
import requests


# ============================================================
# CONFIGURATION
# ============================================================

ZERNIO_API_KEY = os.getenv("ZERNIO_API_KEY")

# Your connected Instagram account.
#
# From your successful check_zernio.py result:
# Instagram account = @promptprohub3
#
# IMPORTANT:
# Put the Zernio account ID in Railway Variables.
#
# Variable:
# ZERNIO_INSTAGRAM_ACCOUNT_ID
#
ZERNIO_INSTAGRAM_ACCOUNT_ID = os.getenv(
    "ZERNIO_INSTAGRAM_ACCOUNT_ID"
)

ZERNIO_BASE_URL = "https://zernio.com/api/v1"


# ============================================================
# VALIDATE CONFIG
# ============================================================

def validate_config():

    if not ZERNIO_API_KEY:
        raise RuntimeError(
            "ZERNIO_API_KEY is missing from Railway Variables."
        )

    if not ZERNIO_INSTAGRAM_ACCOUNT_ID:
        raise RuntimeError(
            "ZERNIO_INSTAGRAM_ACCOUNT_ID is missing "
            "from Railway Variables."
        )


# ============================================================
# HEADERS
# ============================================================

def get_headers():

    return {
        "Authorization": f"Bearer {ZERNIO_API_KEY}",
        "Accept": "application/json"
    }


# ============================================================
# UPLOAD VIDEO TO ZERNIO
# ============================================================

def upload_video(video_path):

    validate_config()

    if not video_path:
        raise ValueError(
            "No video path was supplied."
        )

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Instagram video not found: {video_path}"
        )

    file_size = os.path.getsize(video_path)

    # Zernio direct media upload limit is 25 MB.
    max_size = 25 * 1024 * 1024

    if file_size > max_size:

        size_mb = round(
            file_size / (1024 * 1024),
            2
        )

        raise ValueError(
            f"Video is {size_mb} MB. "
            "Zernio direct media upload is limited "
            "to 25 MB. Use a public CDN/media URL "
            "for larger videos."
        )

    mime_type = (
        mimetypes.guess_type(video_path)[0]
        or "video/mp4"
    )

    url = (
        f"{ZERNIO_BASE_URL}"
        "/media/upload-direct"
    )

    print("=" * 60)
    print("ZERNIO MEDIA UPLOAD")
    print("=" * 60)

    print(
        "Video:",
        video_path
    )

    print(
        "Size:",
        round(
            file_size / (1024 * 1024),
            2
        ),
        "MB"
    )

    print(
        "MIME:",
        mime_type
    )

    try:

        with open(
            video_path,
            "rb"
        ) as video_file:

            files = {
                "file": (
                    os.path.basename(video_path),
                    video_file,
                    mime_type
                )
            }

            data = {
                "contentType": mime_type
            }

            response = requests.post(

                url,

                headers=get_headers(),

                files=files,

                data=data,

                timeout=300

            )

    except requests.RequestException as e:

        raise RuntimeError(
            f"Zernio media upload request failed: {e}"
        )


    print(
        "HTTP STATUS:",
        response.status_code
    )


    try:

        result = response.json()

    except ValueError:

        raise RuntimeError(
            "Zernio returned an invalid response:\n"
            + response.text
        )


    if response.status_code != 200:

        raise RuntimeError(
            "Zernio media upload failed:\n"
            + str(result)
        )


    media_url = result.get("url")

    if not media_url:

        raise RuntimeError(
            "Zernio upload succeeded but "
            "no media URL was returned:\n"
            + str(result)
        )


    print(
        "MEDIA URL RECEIVED:"
    )

    print(
        media_url
    )

    print("=" * 60)


    return media_url


# ============================================================
# PUBLISH INSTAGRAM REEL
# ============================================================

def publish_instagram_reel(
    video_path,
    caption
):

    validate_config()


    if not caption:
        caption = ""


    # --------------------------------------------------------
    # STEP 1 — Upload video
    # --------------------------------------------------------

    media_url = upload_video(
        video_path
    )


    # --------------------------------------------------------
    # STEP 2 — Create Instagram Reel
    # --------------------------------------------------------

    url = (
        f"{ZERNIO_BASE_URL}"
        "/posts"
    )


    request_id = str(
        uuid.uuid4()
    )


    headers = get_headers()

    headers.update({

        "Content-Type":
            "application/json",

        "x-request-id":
            request_id

    })


    payload = {

        "content":
            caption,

        "mediaItems": [

            {
                "type":
                    "video",

                "url":
                    media_url
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

                    # Your videos are produced
                    # by the AI Content Factory.
                    "isAiGenerated":
                        True
                }
            }

        ],

        "publishNow":
            True
    }


    print("=" * 60)
    print("INSTAGRAM REEL PUBLISH")
    print("=" * 60)

    print(
        "Instagram Account:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
    )

    print(
        "Caption:",
        caption
    )

    print(
        "Publishing..."
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
            f"Instagram publishing request failed: {e}"
        )


    print(
        "HTTP STATUS:",
        response.status_code
    )


    try:

        result = response.json()

    except ValueError:

        raise RuntimeError(
            "Zernio returned invalid JSON:\n"
            + response.text
        )


    print(
        "ZERNIO RESPONSE:"
    )

    print(
        result
    )


    if response.status_code not in (
        200,
        201
    ):

        raise RuntimeError(
            "Instagram Reel publishing failed:\n"
            + str(result)
        )


    post = result.get(
        "post",
        {}
    )


    post_id = post.get(
        "_id"
    )


    print("=" * 60)
    print("INSTAGRAM REEL PUBLISHED SUCCESSFULLY")
    print("=" * 60)


    if post_id:

        print(
            "Zernio Post ID:",
            post_id
        )


    # Some successful responses contain
    # platformPostUrl after immediate publishing.

    platform_url = None

    for platform in post.get(
        "platforms",
        []
    ):

        if (
            platform.get("platform")
            == "instagram"
        ):

            platform_url = platform.get(
                "platformPostUrl"
            )

            break


    if platform_url:

        print(
            "Instagram URL:",
            platform_url
        )


    print("=" * 60)


    return result


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================
#
# This lets the main production system call:
#
# publish_to_instagram(video, caption)
#
# without needing to know the internal function name.
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

    validate_config()

    print(
        "ZERNIO_API_KEY: configured"
    )

    print(
        "INSTAGRAM ACCOUNT ID:",
        ZERNIO_INSTAGRAM_ACCOUNT_ID
    )

    print(
        "Instagram uploader is ready."
    )

    print("=" * 60)
