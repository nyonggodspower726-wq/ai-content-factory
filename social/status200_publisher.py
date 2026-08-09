import os
import requests


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

        "platform": "instagram"
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
# PUBLISH TO ONE STATUS 200 ACCOUNT
# ============================================================

def _publish_one_account(
    video_url,
    caption,
    account
):

    account_number = account["number"]

    api_key = account["api_key"]

    account_name = account["account"]

    platform = account["platform"]


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
    # CHECK API KEY
    # ========================================================

    if not api_key:

        raise RuntimeError(
            f"STATUS200_API_KEY_{account_number} "
            "is not configured in Railway."
        )


    # ========================================================
    # CHECK ACCOUNT
    # ========================================================

    if not account_name:

        raise RuntimeError(
            f"STATUS200_ACCOUNT_{account_number} "
            "is not configured in Railway."
        )


    # ========================================================
    # HEADERS
    # ========================================================

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"

    }


    # ========================================================
    # STEP 1 — MEDIA UPLOAD
    # ========================================================

    print()
    print(
        f"[Account {account_number}] "
        "Uploading media to Status 200..."
    )


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
        f"[Account {account_number}] "
        "Media HTTP status:",
        upload_response.status_code
    )


    print(
        f"[Account {account_number}] "
        "Media response:",
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
            f"media JSON: {e}"
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

    )


    if not file_id:

        raise RuntimeError(

            "Status 200 did not return "
            f"a media/file ID: {upload_data}"

        )


    print(
        f"[Account {account_number}] "
        "Media ID:",
        file_id
    )


    # ========================================================
    # STEP 2 — BUILD PLATFORM POST
    # ========================================================

    print()
    print(
        f"[Account {account_number}] "
        f"Preparing {platform.upper()} post..."
    )


    post_data = {

        "accountId":
            account_name,

        "platform":
            platform,

        "content": {

            "text":
                caption,

            "mediaID": [

                file_id

            ]

        }

    }


    # ========================================================
    # TIKTOK SETTINGS
    # ========================================================

    if platform.lower() == "tiktok":

        post_data["tiktok"] = {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }


    # ========================================================
    # INSTAGRAM SETTINGS
    # ========================================================

    if platform.lower() == "instagram":

        post_data["instagram"] = {

            "mediaType":
                "REELS"

        }


    # ========================================================
    # FINAL PUBLISH PAYLOAD
    # ========================================================

    publish_payload = {

        "post":
            post_data

    }


    print(
        f"[Account {account_number}] "
        "Sending publish request..."
    )


    # ========================================================
    # STEP 3 — PUBLISH
    # ========================================================

    publish_response = requests.post(

        f"{STATUS200_BASE_URL}"
        "/api-posts",

        headers=headers,

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
            f"publish JSON: {e}"
        )


    # ========================================================
    # SUCCESS
    # ========================================================

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

        "success": True,

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
# PUBLISH ONE VIDEO TO ALL STATUS 200 ACCOUNTS
# ============================================================

def publish_to_status200(
    video_path,
    caption
):

    print()
    print("=" * 60)
    print("PROMPTPROHUB STATUS 200 MULTI-ACCOUNT PUBLISHER")
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
    # GET RAILWAY PUBLIC URL
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
    # SEND TO EACH ACCOUNT
    # ========================================================

    for account in ACCOUNTS:

        account_number = account["number"]

        platform = account["platform"]

        account_name = account["account"]


        print()
        print("=" * 60)

        print(
            f"STARTING ACCOUNT {account_number}/4"
        )

        print("=" * 60)


        try:

            result = _publish_one_account(

                video_url,

                caption,

                account

            )


            successful.append(
                result
            )


        except Exception as e:

            error = {

                "success": False,

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


            # =================================================
            # IMPORTANT:
            # DO NOT STOP THE OTHER ACCOUNTS
            # =================================================

            print()
            print(
                f"FAILED — ACCOUNT {account_number}"
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
                "Continuing to next Status 200 account..."
            )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 60)
    print("STATUS 200 MULTI-ACCOUNT SUMMARY")
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
        print("SUCCESSFUL ACCOUNTS:")


        for item in successful:

            print(

                f"  Account {item['account_number']} "
                f"→ {item['platform']} "
                f"→ {item['account']}"

            )


    # ========================================================
    # FAILED LIST
    # ========================================================

    if failed:

        print()
        print("FAILED ACCOUNTS:")


        for item in failed:

            print(

                f"  Account {item['account_number']} "
                f"→ {item['platform']} "
                f"→ {item['account']} "
                f"→ {item['error']}"

            )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    print()
    print("=" * 60)


    if successful:

        print(
            "STATUS 200 MULTI-ACCOUNT PUBLISH COMPLETED"
        )

    else:

        print(
            "STATUS 200 MULTI-ACCOUNT PUBLISH FAILED"
        )


    print("=" * 60)


    # ========================================================
    # RETURN EVERYTHING TO BOT.PY
    # ========================================================

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
