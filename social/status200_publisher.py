import os
import requests
import tempfile
import subprocess


# ============================================================
# STATUS 200 CONFIGURATION
# ============================================================

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
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
# EXTRACT PINTEREST IMAGE FROM VIDEO
# ============================================================

def create_pinterest_image(
    video_path
):

    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    output_dir = os.path.join(
        os.path.dirname(video_path),
        "pinterest"
    )


    os.makedirs(
        output_dir,
        exist_ok=True
    )


    filename = os.path.splitext(
        os.path.basename(video_path)
    )[0]


    image_path = os.path.join(
        output_dir,
        f"{filename}_pinterest.jpg"
    )


    print()
    print("=" * 60)
    print("CREATING PINTEREST IMAGE")
    print("=" * 60)

    print(
        "Source video:",
        video_path
    )

    print(
        "Pinterest image:",
        image_path
    )


    # ========================================================
    # FFmpeg
    # ========================================================

    command = [

        "ffmpeg",

        "-y",

        "-i",
        video_path,

        # Grab a frame around 2 seconds into the video.
        "-ss",
        "2",

        "-frames:v",
        "1",

        # Pinterest-friendly JPEG quality.
        "-q:v",
        "2",

        image_path

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
            "FFmpeg is not installed or "
            "is not available in Railway."
        )

    except subprocess.TimeoutExpired:

        raise RuntimeError(
            "FFmpeg timed out while creating "
            "the Pinterest image."
        )


    if result.returncode != 0:

        raise RuntimeError(
            "FFmpeg failed to create Pinterest image:\n"
            + result.stderr[-3000:]
        )


    if not os.path.exists(image_path):

        raise RuntimeError(
            "FFmpeg completed but the Pinterest "
            "JPG was not created."
        )


    image_size = os.path.getsize(
        image_path
    )


    print(
        "Pinterest JPG created."
    )

    print(
        "Image size:",
        round(
            image_size / (1024 * 1024),
            2
        ),
        "MB"
    )

    print("=" * 60)


    return image_path


# ============================================================
# UPLOAD MEDIA TO STATUS 200
# ============================================================

def upload_media(
    media_url,
    api_key,
    account_number
):

    print()
    print(
        f"[Account {account_number}] "
        "Uploading media to Status 200..."
    )


    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"

    }


    response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-media-upload",

        headers=headers,

        json={
            "url": media_url
        },

        timeout=120

    )


    print(
        f"[Account {account_number}] "
        "Media HTTP status:",
        response.status_code
    )


    print(
        f"[Account {account_number}] "
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
        f"[Account {account_number}] "
        "Media ID:",
        file_id
    )


    return file_id


# ============================================================
# PUBLISH ONE STATUS 200 ACCOUNT
# ============================================================

def _publish_one_account(
    media_url,
    caption,
    account,
    pinterest=False
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


    # ========================================================
    # API KEY
    # ========================================================

    if not api_key:

        raise RuntimeError(
            f"STATUS200_API_KEY_{account_number} "
            "is not configured in Railway."
        )


    # ========================================================
    # ACCOUNT
    # ========================================================

    if not account_name:

        raise RuntimeError(
            f"STATUS200_ACCOUNT_{account_number} "
            "is not configured in Railway."
        )


    # ========================================================
    # PINTEREST BOARD
    # ========================================================

    if platform == "pinterest":

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
    # MEDIA UPLOAD
    # ========================================================

    file_id = upload_media(

        media_url,

        api_key,

        account_number

    )


    # ========================================================
    # BASIC POST
    # ========================================================

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


    # ========================================================
    # TIKTOK
    # ========================================================

    if platform == "tiktok":

        post_data["tiktok"] = {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }


    # ========================================================
    # PINTEREST
    # ========================================================

    if platform == "pinterest":

        post_data["pinterest"] = {

            "board_id":
                PINTEREST_BOARD_ID

        }


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
            file_id
        )

        print("=" * 60)


    # ========================================================
    # FINAL PAYLOAD
    # ========================================================

    publish_payload = {

        "post":
            post_data

    }


    print()
    print(
        f"[Account {account_number}] "
        f"Publishing to {platform.upper()}..."
    )


    publish_response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-posts",

        headers={

            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json"

        },

        json=publish_payload,

        timeout=120

    )


    print(
        f"[Account {account_number}] "
        "Publish HTTP status:",
        publish_response.status_code
    )


    print(
        f"[Account {account_number}] "
        "Publish response:",
        publish_response.text
    )


    if not publish_response.ok:

        raise RuntimeError(
            "Status 200 publish failed: "
            + publish_response.text
        )


    try:

        result = publish_response.json()

    except Exception as e:

        raise RuntimeError(
            "Status 200 returned invalid "
            f"publish JSON: {e}"
        )


    # ========================================================
    # SUCCESS
    # ========================================================

    print()
    print("=" * 60)

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

    print("=" * 60)


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
# MAIN PUBLISH FUNCTION
# ============================================================

def publish_to_status200(
    video_path,
    caption
):

    print()
    print("=" * 60)

    print(
        "PROMPTPROHUB STATUS 200 "
        "MULTI-ACCOUNT PUBLISHER"
    )

    print("=" * 60)


    # ========================================================
    # CHECK VIDEO
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
    # RAILWAY URL
    # ========================================================

    base_url = get_railway_public_url()


    filename = os.path.basename(
        video_path
    )


    video_url = (
        f"{base_url}/videos/{filename}"
    )


    print()
    print(
        "Local video:",
        video_path
    )

    print(
        "Railway URL:",
        base_url
    )

    print(
        "Public video URL:",
        video_url
    )


    # ========================================================
    # RESULTS
    # ========================================================

    successful = []

    failed = []


    # ========================================================
    # PROCESS EACH ACCOUNT
    # ========================================================

    for account in ACCOUNTS:

        account_number = account["number"]

        platform = (
            account["platform"].lower()
        )

        account_name = account["account"]


        print()
        print("=" * 60)

        print(
            f"STARTING ACCOUNT "
            f"{account_number}/{len(ACCOUNTS)}"
        )

        print("=" * 60)


        try:

            # ==================================================
            # PINTEREST
            # ==================================================

            if platform == "pinterest":

                print()
                print(
                    "Pinterest detected."
                )

                print(
                    "The MP4 will NOT be sent "
                    "directly to Pinterest."
                )

                # ----------------------------------------------
                # Create JPG
                # ----------------------------------------------

                pinterest_image = (
                    create_pinterest_image(
                        video_path
                    )
                )


                # ----------------------------------------------
                # Create public URL for JPG
                # ----------------------------------------------

                image_filename = (
                    os.path.basename(
                        pinterest_image
                    )
                )


                image_url = (
                    f"{base_url}"
                    f"/videos/pinterest/"
                    f"{image_filename}"
                )


                print()
                print(
                    "Pinterest public image URL:",
                    image_url
                )


                # ----------------------------------------------
                # Publish JPG
                # ----------------------------------------------

                result = _publish_one_account(

                    image_url,

                    caption,

                    account,

                    pinterest=True

                )


            # ==================================================
            # ALL OTHER PLATFORMS
            # ==================================================

            else:

                result = _publish_one_account(

                    video_url,

                    caption,

                    account,

                    pinterest=False

                )


            successful.append(
                result
            )


            print()
            print(
                f"Status 200 Account "
                f"{account_number} → "
                f"{platform} completed."
            )


        except Exception as e:

            error = {

                "success":
                    False,

                "account_number":
                    account_number,

                "account":
                    account_name,

                "platform":
                    platform,

                "error":
                    str(e)

            }


            failed.append(
                error
            )


            print()
            print("=" * 60)

            print(
                f"FAILED — ACCOUNT "
                f"{account_number}"
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
                "Error:",
                str(e)
            )

            print(
                "Continuing to next account..."
            )

            print("=" * 60)


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 60)

    print(
        "STATUS 200 MULTI-ACCOUNT SUMMARY"
    )

    print("=" * 60)

    print(
        "Total accounts:",
        len(ACCOUNTS)
    )

    print(
        "Successful:",
        len(successful)
    )

    print(
        "Failed:",
        len(failed)
    )


    # ========================================================
    # SUCCESS LIST
    # ========================================================

    if successful:

        print()
        print(
            "SUCCESSFUL ACCOUNTS:"
        )


        for item in successful:

            print(
                f"  Account "
                f"{item['account_number']} "
                f"→ {item['platform']} "
                f"→ {item['account']}"
            )


    # ========================================================
    # FAILED LIST
    # ========================================================

    if failed:

        print()
        print(
            "FAILED ACCOUNTS:"
        )


        for item in failed:

            print(
                f"  Account "
                f"{item['account_number']} "
                f"→ {item['platform']} "
                f"→ {item['account']} "
                f"→ {item['error']}"
            )


    # ========================================================
    # FINAL
    # ========================================================

    print()
    print("=" * 60)


    if successful:

        print(
            "STATUS 200 MULTI-ACCOUNT "
            "PUBLISH COMPLETED"
        )

    else:

        print(
            "STATUS 200 MULTI-ACCOUNT "
            "PUBLISH FAILED"
        )


    print("=" * 60)


    return {

        "success":
            len(successful) > 0,

        "total":
            len(ACCOUNTS),

        "successful":
            successful,

        "failed":
            failed

}
