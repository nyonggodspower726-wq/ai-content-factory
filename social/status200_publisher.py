import os
import subprocess
import requests


# ============================================================
# PROMPTPROHUB STATUS 200 MULTI-ACCOUNT PUBLISHER
# ============================================================
#
# ACCOUNT 1  -> TikTok
# ACCOUNT 2  -> LinkedIn
# ACCOUNT 3  -> TikTok
# ACCOUNT 4  -> Pinterest
#
# IMPORTANT:
#
# Accounts 1-3 continue using the generated MP4.
#
# Pinterest is different:
#
# Pinterest requires an IMAGE PIN.
#
# Therefore Account 4 automatically:
#
# 1. Takes the generated MP4
# 2. Extracts a JPG frame
# 3. Makes the JPG publicly accessible through Railway
# 4. Uploads the JPG to Status 200
# 5. Publishes the JPG to Pinterest
#
# ============================================================


# ============================================================
# STATUS 200 CONFIGURATION
# ============================================================

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
)


# ============================================================
# STATUS 200 REST V2
# ============================================================

STATUS200_V2_URL = (
    "https://status200uploads.com/api/v2/posts"
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
        "Railway public domain is not available. "
        "Set RAILWAY_PUBLIC_DOMAIN or "
        "RAILWAY_PUBLIC_URL in Railway Variables."
    )


# ============================================================
# PINTEREST BOARD ID
# ============================================================

PINTEREST_BOARD_ID = os.getenv(
    "STATUS200_PINTEREST_BOARD_ID"
)


# ============================================================
# STATUS 200 ACCOUNTS
# ============================================================

ACCOUNTS = [

    {
        "number": 1,

        "api_key": os.getenv(
            "STATUS200_API_KEY_1"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_1"
        ),

        "platform": "tiktok"
    },


    {
        "number": 2,

        "api_key": os.getenv(
            "STATUS200_API_KEY_2"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_2"
        ),

        "platform": "linkedin"
    },


    {
        "number": 3,

        "api_key": os.getenv(
            "STATUS200_API_KEY_3"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_3"
        ),

        "platform": "tiktok"
    },


    {
        "number": 4,

        "api_key": os.getenv(
            "STATUS200_API_KEY_4"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_4"
        ),

        "platform": "pinterest"
    }

]


# ============================================================
# CREATE PINTEREST JPG
# ============================================================

def create_pinterest_jpg(
    video_path
):

    if not video_path:

        raise ValueError(
            "No video path supplied for Pinterest."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    # --------------------------------------------------------
    # Pinterest output directory
    # --------------------------------------------------------

    output_dir = os.path.join(
        "output",
        "videos",
        "pinterest"
    )


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Create JPG filename
    # --------------------------------------------------------

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]


    jpg_path = os.path.join(
        output_dir,
        f"{video_name}_pinterest.jpg"
    )


    print()
    print("=" * 60)
    print("CREATING PINTEREST JPG")
    print("=" * 60)

    print(
        "Source video:",
        video_path
    )

    print(
        "Pinterest JPG:",
        jpg_path
    )


    # --------------------------------------------------------
    # Use FFmpeg
    #
    # Take frame at 1 second.
    #
    # If the video is shorter than 1 second,
    # FFmpeg automatically falls back to the available frame.
    # --------------------------------------------------------

    command = [

        "ffmpeg",

        "-y",

        "-ss",
        "1",

        "-i",
        video_path,

        "-frames:v",
        "1",

        "-q:v",
        "2",

        jpg_path

    ]


    try:

        result = subprocess.run(

            command,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True,

            timeout=120

        )

    except FileNotFoundError:

        raise RuntimeError(
            "FFmpeg is not installed or not available "
            "in the Railway environment."
        )

    except subprocess.TimeoutExpired:

        raise RuntimeError(
            "FFmpeg timed out while creating "
            "the Pinterest JPG."
        )


    # --------------------------------------------------------
    # Check FFmpeg
    # --------------------------------------------------------

    if result.returncode != 0:

        print(
            "FFmpeg output:"
        )

        print(
            result.stderr[-4000:]
        )

        raise RuntimeError(
            "FFmpeg failed to create the "
            "Pinterest JPG."
        )


    # --------------------------------------------------------
    # Check JPG
    # --------------------------------------------------------

    if not os.path.exists(jpg_path):

        raise RuntimeError(
            "Pinterest JPG was not created."
        )


    jpg_size = os.path.getsize(
        jpg_path
    )


    if jpg_size <= 0:

        raise RuntimeError(
            "Pinterest JPG was created but "
            "has zero bytes."
        )


    print(
        "Pinterest JPG created successfully."
    )

    print(
        "JPG size:",
        round(
            jpg_size / (1024 * 1024),
            2
        ),
        "MB"
    )

    print("=" * 60)


    return jpg_path


# ============================================================
# CREATE PUBLIC URL FOR FILE
# ============================================================

def get_public_file_url(
    file_path
):

    base_url = get_railway_public_url()


    filename = os.path.basename(
        file_path
    )


    # --------------------------------------------------------
    # Railway static video directory
    #
    # Your Railway server already exposes:
    #
    # /videos/...
    #
    # Keep the Pinterest JPG under the same public directory.
    # --------------------------------------------------------

    relative_path = os.path.relpath(
        file_path,
        "output"
    )


    relative_path = (
        relative_path
        .replace("\\", "/")
    )


    return (
        f"{base_url}/videos/"
        f"{relative_path}"
    )


# ============================================================
# UPLOAD MEDIA TO STATUS 200
# ============================================================

def upload_media(
    video_url,
    api_key
):

    if not video_url:

        raise ValueError(
            "No public media URL supplied."
        )


    if not api_key:

        raise RuntimeError(
            "Status 200 API key is missing."
        )


    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"

    }


    print()
    print(
        "Uploading media to Status 200..."
    )

    print(
        "Media URL:",
        video_url
    )


    response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-media-upload",

        headers=headers,

        json={
            "url": video_url
        },

        timeout=180

    )


    print(
        "Media HTTP status:",
        response.status_code
    )


    print(
        "Media response:",
        response.text
    )


    if not response.ok:

        raise RuntimeError(

            "Status 200 media upload failed: "
            + response.text

        )


    try:

        data = response.json()

    except Exception as e:

        raise RuntimeError(
            "Status 200 returned invalid "
            f"media JSON: {e}"
        )


    file_id = (

        data.get("file_id")

        or data.get("mediaID")

        or data.get("mediaId")

    )


    if not file_id:

        raise RuntimeError(

            "Status 200 did not return "
            f"a media/file ID: {data}"

        )


    print(
        "Status 200 Media ID:",
        file_id
    )


    return file_id


# ============================================================
# PUBLISH NORMAL VIDEO ACCOUNT
# ============================================================

def _publish_video_account(
    video_url,
    caption,
    account
):

    account_number = account["number"]

    api_key = account["api_key"]

    account_name = account["account"]

    platform = account["platform"].lower()


    print()
    print("=" * 60)

    print(
        f"STATUS 200 ACCOUNT {account_number}"
    )

    print("=" * 60)

    print(
        "Account:",
        account_name
    )

    print(
        "Platform:",
        platform
    )


    # --------------------------------------------------------
    # API KEY
    # --------------------------------------------------------

    if not api_key:

        raise RuntimeError(
            f"STATUS200_API_KEY_{account_number} "
            "is not configured in Railway."
        )


    # --------------------------------------------------------
    # ACCOUNT
    # --------------------------------------------------------

    if not account_name:

        raise RuntimeError(
            f"STATUS200_ACCOUNT_{account_number} "
            "is not configured in Railway."
        )


    # --------------------------------------------------------
    # UPLOAD VIDEO
    # --------------------------------------------------------

    file_id = upload_media(
        video_url,
        api_key
    )


    # --------------------------------------------------------
    # BASIC POST
    # --------------------------------------------------------

    post_data = {

        "accountId":
            account_name,

        "platform":
            platform,

        "content": {

            "text":
                caption or "",

            "mediaID": [

                file_id

            ]

        }

    }


    # --------------------------------------------------------
    # TIKTOK
    # --------------------------------------------------------

    if platform == "tiktok":

        post_data["tiktok"] = {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }


    # --------------------------------------------------------
    # LINKEDIN
    # --------------------------------------------------------

    if platform == "linkedin":

        pass


    # --------------------------------------------------------
    # PUBLISH NORMAL ACCOUNT
    # --------------------------------------------------------

    print()
    print(
        f"Publishing Account {account_number} "
        f"to {platform.upper()}..."
    )


    response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-posts",

        headers={

            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json"

        },

        json={
            "post":
                post_data
        },

        timeout=180

    )


    print(
        "Publish HTTP status:",
        response.status_code
    )


    print(
        "Publish response:",
        response.text
    )


    if not response.ok:

        raise RuntimeError(

            "Status 200 publish failed: "
            + response.text

        )


    try:

        result = response.json()

    except Exception as e:

        raise RuntimeError(
            "Status 200 returned invalid "
            f"publish JSON: {e}"
        )


    print()
    print(
        f"SUCCESS — ACCOUNT {account_number}"
    )

    print(
        "Platform:",
        platform
    )

    print(
        "Account:",
        account_name
    )

    print(
        "Result:",
        result
    )


    return {

        "success":
            True,

        "account_number":
            account_number,

        "account":
            account_name,

        "platform":
            platform,

        "result":
            result

    }


# ============================================================
# PUBLISH PINTEREST ONLY
# ============================================================

def _publish_pinterest(
    video_path,
    caption,
    account
):

    account_number = account["number"]

    api_key = account["api_key"]

    account_name = account["account"]


    print()
    print("=" * 60)
    print("PINTEREST ACCOUNT 4")
    print("=" * 60)

    print(
        "Account:",
        account_name
    )

    print(
        "Platform:",
        "pinterest"
    )


    # ========================================================
    # API KEY
    # ========================================================

    if not api_key:

        raise RuntimeError(
            "STATUS200_API_KEY_4 "
            "is not configured in Railway."
        )


    # ========================================================
    # ACCOUNT
    # ========================================================

    if not account_name:

        raise RuntimeError(
            "STATUS200_ACCOUNT_4 "
            "is not configured in Railway."
        )


    # ========================================================
    # BOARD ID
    # ========================================================

    if not PINTEREST_BOARD_ID:

        raise RuntimeError(
            "STATUS200_PINTEREST_BOARD_ID "
            "is missing from Railway Variables."
        )


    print(
        "Pinterest Board ID:",
        PINTEREST_BOARD_ID
    )


    # ========================================================
    # STEP 1 — CREATE JPG
    # ========================================================

    pinterest_jpg = (
        create_pinterest_jpg(
            video_path
        )
    )


    # ========================================================
    # STEP 2 — CREATE PUBLIC JPG URL
    # ========================================================

    pinterest_url = (
        get_public_file_url(
            pinterest_jpg
        )
    )


    print()
    print(
        "Pinterest JPG public URL:"
    )

    print(
        pinterest_url
    )


    # ========================================================
    # STEP 3 — CHECK PUBLIC JPG
    # ========================================================

    print()
    print(
        "Checking public Pinterest JPG..."
    )


    try:

        check = requests.head(

            pinterest_url,

            timeout=60,

            allow_redirects=True

        )

    except requests.RequestException as e:

        raise RuntimeError(
            "Could not check Pinterest JPG URL: "
            + str(e)
        )


    print(
        "Pinterest JPG HTTP status:",
        check.status_code
    )


    if not check.ok:

        raise RuntimeError(

            "Pinterest JPG is not publicly reachable. "
            f"HTTP {check.status_code}: "
            f"{pinterest_url}"

        )


    # ========================================================
    # STEP 4 — UPLOAD JPG
    # ========================================================

    pinterest_media_id = (
        upload_media(
            pinterest_url,
            api_key
        )
    )


    # ========================================================
    # STEP 5 — PINTEREST PAYLOAD
    # ========================================================

    #
    # IMPORTANT:
    #
    # Pinterest receives an IMAGE media ID.
    #
    # We intentionally do NOT send the original MP4.
    #
    # The board ID is supplied in the Pinterest-specific
    # options.
    #
    # ========================================================

    pinterest_post = {

        "accountId":
            account_name,

        "platform":
            "pinterest",

        "content": {

            "text":
                caption or "",

            "mediaID": [

                pinterest_media_id

            ]

        },

        "pinterest": {

            "boardId":
                PINTEREST_BOARD_ID,

            "board_id":
                PINTEREST_BOARD_ID

        }

    }


    # ========================================================
    # DEBUG
    # ========================================================

    print()
    print("=" * 60)
    print("PINTEREST PUBLISH DATA")
    print("=" * 60)

    print(
        "Pinterest Account:",
        account_name
    )

    print(
        "Pinterest Board ID:",
        PINTEREST_BOARD_ID
    )

    print(
        "Pinterest Media ID:",
        pinterest_media_id
    )

    print(
        "Pinterest Payload:",
        pinterest_post
    )

    print("=" * 60)


    # ========================================================
    # STEP 6 — PUBLISH USING REST V2
    # ========================================================

    print()
    print(
        "Publishing Pinterest Pin..."
    )

    print(
        "Endpoint:",
        STATUS200_V2_URL
    )


    response = requests.post(

        STATUS200_V2_URL,

        headers={

            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json"

        },

        json={

            "post":
                pinterest_post

        },

        timeout=180

    )


    print()
    print(
        "Pinterest Publish HTTP status:",
        response.status_code
    )


    print(
        "Pinterest Publish response:",
        response.text
    )


    # ========================================================
    # ACCEPT 200 OR 202
    # ========================================================

    if response.status_code not in (
        200,
        201,
        202
    ):

        raise RuntimeError(

            "Status 200 Pinterest publish failed: "
            + response.text

        )


    # ========================================================
    # PARSE RESPONSE
    # ========================================================

    try:

        result = response.json()

    except Exception:

        result = {
            "raw_response":
                response.text
        }


    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("=" * 60)

    if response.status_code == 202:

        print(
            "PINTEREST ACCEPTED / QUEUED"
        )

    else:

        print(
            "PINTEREST PUBLISHED SUCCESSFULLY"
        )

    print("=" * 60)

    print(
        "Account:",
        account_name
    )

    print(
        "Board:",
        PINTEREST_BOARD_ID
    )

    print(
        "JPG:",
        pinterest_jpg
    )

    print(
        "Result:",
        result
    )

    print("=" * 60)


    ret
