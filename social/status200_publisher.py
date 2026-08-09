import os
import requests


# ============================================================
# STATUS 200 CONFIGURATION
# ============================================================

STATUS200_BASE_URL = (
    "https://app.status200uploads.com/functions/v1"
)


# ============================================================
# RAILWAY PUBLIC DOMAIN
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
        "Railway public domain is not available."
    )


# ============================================================
# FOUR STATUS 200 ACCOUNTS
# ============================================================

ACCOUNTS = [

    {
        "api_key": os.getenv(
            "STATUS200_API_KEY_1"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_1"
        ),

        "platform": "tiktok"
    },


    {
        "api_key": os.getenv(
            "STATUS200_API_KEY_2"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_2"
        ),

        "platform": "linkedin"
    },


    {
        "api_key": os.getenv(
            "STATUS200_API_KEY_3"
        ),

        "account": os.getenv(
            "STATUS200_ACCOUNT_3"
        ),

        "platform": "instagram"
    },


    {
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
# PUBLISH ONE VIDEO
# ============================================================

def publish_to_status200(
    video_path,
    caption,
    account_number=1
):

    print("=" * 60)
    print("STATUS 200 PUBLISHER")
    print("=" * 60)


    # --------------------------------------------------------
    # ACCOUNT NUMBER
    # --------------------------------------------------------

    if account_number < 1 or account_number > 4:

        raise ValueError(
            "account_number must be between 1 and 4."
        )


    selected = ACCOUNTS[
        account_number - 1
    ]


    api_key = selected["api_key"]

    account = selected["account"]

    platform = selected["platform"]


    # --------------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------------

    if not api_key:

        raise RuntimeError(
            f"STATUS200_API_KEY_{account_number} "
            "is not configured in Railway."
        )


    # --------------------------------------------------------
    # CHECK ACCOUNT
    # --------------------------------------------------------

    if not account:

        raise RuntimeError(
            f"STATUS200_ACCOUNT_{account_number} "
            "is not configured in Railway."
        )


    # --------------------------------------------------------
    # CHECK VIDEO
    # --------------------------------------------------------

    if not video_path:

        raise ValueError(
            "No video path provided."
        )


    if not os.path.exists(video_path):

        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )


    # --------------------------------------------------------
    # RAILWAY URL
    # --------------------------------------------------------

    base_url = get_railway_public_url()


    filename = os.path.basename(
        video_path
    )


    video_url = (
        f"{base_url}/videos/{filename}"
    )


    print(
        "Account number:",
        account_number
    )

    print(
        "Status 200 account:",
        account
    )

    print(
        "Platform:",
        platform
    )

    print(
        "Video URL:",
        video_url
    )


    # --------------------------------------------------------
    # HEADERS
    # --------------------------------------------------------

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"

    }


    # ========================================================
    # STEP 1 — MEDIA UPLOAD
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


    try:

        upload_data = (
            upload_response.json()
        )

    except Exception:

        raise RuntimeError(
            "Status 200 returned invalid "
            "media upload JSON."
        )


    # --------------------------------------------------------
    # GET MEDIA ID
    # --------------------------------------------------------

    file_id = (

        upload_data.get("file_id")

        or upload_data.get("mediaID")

        or upload_data.get("mediaId")

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
    # STEP 2 — CREATE PLATFORM POST
    # ========================================================

    print("=" * 60)

    print(
        f"STATUS 200 → {platform.upper()}"
    )

    print("=" * 60)


    post_data = {

        "accountId":
            account,

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


    # --------------------------------------------------------
    # TIKTOK OPTIONS
    # --------------------------------------------------------

    if platform == "tiktok":

        post_data["tiktok"] = {

            "privacyLevel":
                "PUBLIC_TO_EVERYONE"

        }


    # --------------------------------------------------------
    # FINAL PAYLOAD
    # --------------------------------------------------------

    publish_payload = {

        "post":
            post_data

    }


    print(
        "Publishing account:",
        account
    )

    print(
        "Publishing platform:",
        platform
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
            "Status 200 returned invalid "
            "publish JSON."
        )


    # ========================================================
    # SUCCESS
    # ========================================================

    print("=" * 60)

    print(
        "STATUS 200 PUBLISH REQUEST SUCCESSFUL"
    )

    print("=" * 60)


    print(
        "Account:",
        account
    )

    print(
        "Platform:",
        platform
    )

    print(
        "Result:",
        result
    )


    return result
