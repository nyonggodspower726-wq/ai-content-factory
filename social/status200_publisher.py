import os
import requests


# ============================================================
# PROMPTPROHUB ZERNIO THREE-ACCOUNT PUBLISHER
#
# API KEY 1 → Instagram
# API KEY 2 → TikTok
# API KEY 3 → YouTube
#
# Each key independently discovers its own connected account
# from GET /accounts before publishing.
# ============================================================


ZERNIO_BASE_URL = "https://zernio.com/api/v1"


# ============================================================
# THREE ZERNIO API KEYS
# ============================================================

ZERNIO_INSTAGRAM_API_KEY = os.getenv("ZERNIO_API_KEY")
ZERNIO_TIKTOK_API_KEY = os.getenv("ZERNIO_TIKTOK_API_KEY")
ZERNIO_YOUTUBE_API_KEY = os.getenv("ZERNIO_YOUTUBE_API_KEY")


# ============================================================
# OPTIONAL ACCOUNT IDs
#
# We keep these variables for compatibility, but the publisher
# will verify the real account through /accounts first.
# ============================================================

ZERNIO_INSTAGRAM_ACCOUNT_ID = os.getenv(
    "ZERNIO_INSTAGRAM_ACCOUNT_ID"
)

ZERNIO_TIKTOK_ACCOUNT_ID = os.getenv(
    "ZERNIO_TIKTOK_ACCOUNT_ID"
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
# HEADERS
# ============================================================

def get_headers(api_key):

    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }


# ============================================================
# GET RAILWAY URL
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
# BUILD VIDEO URL
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
# DISCOVER ACCOUNT FROM API KEY
# ============================================================

def get_connected_account(
    api_key,
    platform,
    configured_id=None
):

    if not api_key:

        raise RuntimeError(
            f"No Zernio API key configured for {platform}."
        )


    print()
    print("-" * 60)
    print(
        f"CHECKING ZERNIO ACCOUNT → {platform.upper()}"
    )
    print("-" * 60)


    response = requests.get(

        f"{ZERNIO_BASE_URL}/accounts",

        headers=get_headers(api_key),

        timeout=30

    )


    print(
        f"{platform.upper()} /accounts HTTP:",
        response.status_code
    )


    if not response.ok:

        raise RuntimeError(
            f"{platform} account lookup failed: "
            + response.text
        )


    data = response.json()

    accounts = data.get(
        "accounts",
        []
    )


    print(
        f"{platform.upper()} accounts returned:",
        len(accounts)
    )


    # --------------------------------------------------------
    # FIRST: find the configured ID if it exists
    # --------------------------------------------------------

    if configured_id:

        configured_id = str(
            configured_id
        ).strip()


        for account in accounts:

            if str(
                account.get("_id", "")
            ).strip() == configured_id:

                if account.get(
                    "platform"
                ) == platform:

                    if account.get(
                        "isActive",
                        True
                    ):

                        print(
                            "Verified account:",
                            account["_id"]
                        )

                        print(
                            "Username:",
                            account.get(
                                "username"
                            )
                            or account.get(
                                "displayName"
                            )
                            or "N/A"
                        )

                        return account["_id"]


    # --------------------------------------------------------
    # SECOND: automatically find platform
    # --------------------------------------------------------

    matching_accounts = [

        account

        for account in accounts

        if account.get(
            "platform"
        ) == platform

        and account.get(
            "isActive",
            True
        )

    ]


    if not matching_accounts:

        raise RuntimeError(
            f"No active {platform} account "
            f"was found for this API key."
        )


    account = matching_accounts[0]


    account_id = account.get(
        "_id"
    )


    if not account_id:

        raise RuntimeError(
            f"{platform} account has no _id."
        )


    print(
        "Auto-selected account:",
        account_id
    )


    print(
        "Username:",
        account.get(
            "username"
        )
        or account.get(
            "displayName"
        )
        or "N/A"
    )


    return account_id


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


    account_id = get_connected_account(

        ZERNIO_INSTAGRAM_API_KEY,

        "instagram",

        ZERNIO_INSTAGRAM_ACCOUNT_ID

    )


    payload = {

        "content": caption,

        "mediaItems": [

            {
                "type": "video",
                "url": video_url
            }

        ],

        "platforms": [

            {
                "platform": "instagram",

                "accountId": account_id,

                "platformSpecificData": {

                    "isAiGenerated": True

                }

            }

        ],

        "publishNow": True

    }


    print(
        "Publishing Instagram..."
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


    account_id = get_connected_account(

        ZERNIO_TIKTOK_API_KEY,

        "tiktok",

        ZERNIO_TIKTOK_ACCOUNT_ID

    )


    payload = {

        "content": caption,

        "mediaItems": [

            {
                "type": "video",
                "url": video_url
            }

        ],

        "platforms": [

            {
                "platform": "tiktok",

                "accountId": account_id,

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

        "publishNow": True

    }


    print(
        "TikTok account:",
        account_id
    )

    print(
        "Publishing TikTok..."
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


    account_id = get_connected_account(

        ZERNIO_YOUTUBE_API_KEY,

        "youtube",

        ZERNIO_YOUTUBE_ACCOUNT_ID

    )


    title = make_youtube_title(
        caption
    )


    payload = {

        "content": caption,

        "mediaItems": [

            {
                "type": "video",
                "url": video_url
            }

        ],

        "platforms": [

            {
                "platform": "youtube",

                "accountId": account_id,

                "platformSpecificData": {

                    "title": title,

                    "visibility": "public"

                }

            }

        ],

        "publishNow": True

    }


    print(
        "YouTube account:",
        account_id
    )

    print(
        "YouTube title:",
        title
    )

    print(
        "Publishing YouTube..."
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
        "PROMPTPROHUB ZERNIO THREE-KEY PUBLISHER"
    )
    print("=" * 60)


    video_url = get_public_video_url(
        video_path
    )


    print(
        "Public video URL:",
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

        successful.append({

            "platform":
                "instagram",

            "result":
                result

        })

        print(
            "INSTAGRAM → SUCCESS"
        )


    except Exception as e:

        failed.append({

            "platform":
                "instagram",

            "error":
                str(e)

        })

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

        successful.append({

            "platform":
                "tiktok",

            "result":
                result

        })

        print(
            "TIKTOK → SUCCESS"
        )


    except Exception as e:

        failed.append({

            "platform":
                "tiktok",

            "error":
                str(e)

        })

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

        successful.append({

            "platform":
                "youtube",

            "result":
                result

        })

        print(
            "YOUTUBE → SUCCESS"
        )


    except Exception as e:

        failed.append({

            "platform":
                "youtube",

            "error":
                str(e)

        })

        print(
            "YOUTUBE → FAILED:",
            e
        )


    # ========================================================
    # FINAL SUMMARY
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
# CONFIGURATION CHECK
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print(
        "PROMPTPROHUB ZERNIO CONFIGURATION"
    )
    print("=" * 60)


    print(
        "Instagram API:",
        "SET"
        if ZERNIO_INSTAGRAM_API_KEY
        else "MISSING"
    )


    print(
        "TikTok API:",
        "SET"
        if ZERNIO_TIKTOK_API_KEY
        else "MISSING"
    )


    print(
        "YouTube API:",
        "SET"
        if ZERNIO_YOUTUBE_API_KEY
        else "MISSING"
    )


    print("=" * 60)
