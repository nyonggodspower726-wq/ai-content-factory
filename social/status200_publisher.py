import os
import requests

STATUS200_BASE_URL="https://app.status200uploads.com/functions/v1"

# ============================================================
# STATUS 200 — TIKTOK
# ============================================================

STATUS200_TIKTOK_API_KEY=(
    os.getenv("STATUS200_TIKTOK_API_KEY_1")
    or os.getenv("STATUS200_TIKTOK_API_KEY")
    or os.getenv("STATUS200_API_KEY_1")
    or os.getenv("STATUS200_API_KEY")
)

STATUS200_TIKTOK_ACCOUNT=(
    os.getenv("STATUS200_TIKTOK_ACCOUNT_1")
    or os.getenv("STATUS200_TIKTOK_ACCOUNT")
    or os.getenv("STATUS200_ACCOUNT_1")
    or os.getenv("STATUS200_ACCOUNT")
)

# ============================================================
# STATUS 200 — INSTAGRAM
# ============================================================

STATUS200_INSTAGRAM_API_KEY=(
    os.getenv("STATUS200_INSTAGRAM_API_KEY_1")
    or os.getenv("STATUS200_INSTAGRAM_API_KEY")
    or os.getenv("STATUS200_API_KEY_2")
)

STATUS200_INSTAGRAM_ACCOUNT=(
    os.getenv("STATUS200_INSTAGRAM_ACCOUNT_1")
    or os.getenv("STATUS200_INSTAGRAM_ACCOUNT")
    or os.getenv("STATUS200_ACCOUNT_2")
)

# ============================================================
# STATUS 200 — YOUTUBE
# ============================================================

STATUS200_YOUTUBE_API_KEY=(
    os.getenv("STATUS200_YOUTUBE_API_KEY_1")
    or os.getenv("STATUS200_YOUTUBE_API_KEY")
    or os.getenv("STATUS200_API_KEY_3")
)

STATUS200_YOUTUBE_ACCOUNT=(
    os.getenv("STATUS200_YOUTUBE_ACCOUNT_1")
    or os.getenv("STATUS200_YOUTUBE_ACCOUNT")
    or os.getenv("STATUS200_ACCOUNT_3")
)

# ============================================================
# RAILWAY PUBLIC VIDEO URL
# ============================================================

RAILWAY_PUBLIC_DOMAIN=os.getenv("RAILWAY_PUBLIC_DOMAIN")
RAILWAY_PUBLIC_URL=os.getenv("RAILWAY_PUBLIC_URL")

def get_railway_public_url():
    if RAILWAY_PUBLIC_DOMAIN:
        domain=RAILWAY_PUBLIC_DOMAIN.strip()
        if not domain.startswith(("http://","https://")):
            domain="https://"+domain
        return domain.rstrip("/")
    if RAILWAY_PUBLIC_URL:
        url=RAILWAY_PUBLIC_URL.strip()
        if not url.startswith(("http://","https://")):
            url="https://"+url
        return url.rstrip("/")
    raise RuntimeError(
        "Railway public URL is missing. "
        "Configure RAILWAY_PUBLIC_DOMAIN or RAILWAY_PUBLIC_URL."
    )

def get_public_video_url(video_path):
    if not video_path:
        raise ValueError("No video path was provided.")
    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video not found: {video_path}"
        )
    filename=os.path.basename(video_path)
    return f"{get_railway_public_url()}/videos/{filename}"

# ============================================================
# STATUS 200 HEADERS
# ============================================================

def get_status200_headers(api_key):
    if not api_key:
        raise RuntimeError(
            "Status 200 API key is missing from Railway Variables."
        )
    return {
        "Authorization":f"Bearer {api_key}",
        "Content-Type":"application/json",
        "Accept":"application/json"
    }

# ============================================================
# STATUS 200 PROFILE CHECK
# ============================================================

def check_status200_account(api_key,account_id,platform):
    headers=get_status200_headers(api_key)
    url=f"{STATUS200_BASE_URL}/api-posts"
    params={
        "action":"profiles"
    }
    response=requests.get(
        url,
        headers=headers,
        params=params,
        timeout=60
    )
    print(
        f"{platform} Status 200 profile check:",
        response.status_code
    )
    print(
        f"{platform} Status 200 profiles:",
        response.text
    )
    if not response.ok:
        raise RuntimeError(
            f"Status 200 {platform} profile check failed: "
            + response.text
        )
    try:
        data=response.json()
    except Exception as e:
        raise RuntimeError(
            f"Status 200 {platform} profile response was invalid JSON: {e}"
        )
    profiles=data.get("profiles",[])
    if account_id:
        matched=False
        for profile in profiles:
            profile_account=str(
                profile.get("account_id","")
            )
            profile_platform=str(
                profile.get("platform","")
            ).lower()
            if (
                profile_account==str(account_id)
                and profile_platform==platform.lower()
            ):
                matched=True
                break
        if not matched:
            print(
                f"WARNING: Status 200 did not find "
                f"account {account_id} for {platform} "
                f"in the returned profile list."
            )
    return data

# ============================================================
# STATUS 200 MEDIA UPLOAD
# ============================================================

def upload_media_status200(video_url,api_key,platform):
    headers=get_status200_headers(api_key)
    upload_url=f"{STATUS200_BASE_URL}/api-media-upload"
    upload_payload={
        "url":video_url
    }
    print("-"*60)
    print(f"{platform.upper()} — STATUS 200 MEDIA UPLOAD")
    print("-"*60)
    print("Media URL:",video_url)
    response=requests.post(
        upload_url,
        headers=headers,
        json=upload_payload,
        timeout=180
    )
    print(
        f"{platform} media HTTP:",
        response.status_code
    )
    print(
        f"{platform} media response:",
        response.text
    )
    if not response.ok:
        raise RuntimeError(
            f"Status 200 {platform} media upload failed: "
            + response.text
        )
    try:
        data=response.json()
    except Exception as e:
        raise RuntimeError(
            f"Status 200 {platform} returned invalid media JSON: {e}"
        )
    file_id=(
        data.get("file_id")
        or data.get("mediaID")
        or data.get("mediaId")
        or data.get("id")
    )
    if not file_id:
        raise RuntimeError(
            f"Status 200 {platform} media upload succeeded "
            "but no file_id was returned.\n"
            f"Response: {data}"
        )
    print(
        f"{platform} Status 200 file ID:",
        file_id
    )
    return file_id

# ============================================================
# STATUS 200 POST
# ============================================================

def create_status200_post(
    platform,
    account_id,
    api_key,
    file_id,
    caption
):
    headers=get_status200_headers(api_key)
    post_data={
        "accountId":account_id,
        "platform":platform,
        "content":{
            "text":str(caption or "").strip(),
            "mediaID":[file_id]
        }
    }

    if platform=="tiktok":
        post_data["tiktok"]={
            "privacyLevel":"PUBLIC_TO_EVERYONE"
        }

    elif platform=="instagram":
        post_data["instagram"]={
            "postType":"reel",
            "shareToFeed":True
        }

    elif platform=="youtube":
        post_data["youtube"]={
            "visibility":"public"
        }

    publish_url=f"{STATUS200_BASE_URL}/api-posts"

    print("-"*60)
    print(
        f"STATUS 200 → {platform.upper()}"
    )
    print("-"*60)
    print("Status 200 account:",account_id)
    print("Platform:",platform)
    print("Media ID:",file_id)
    print("Endpoint:",publish_url)

    response=requests.post(
        publish_url,
        headers=headers,
        json={
            "post":post_data
        },
        timeout=180
    )

    print(
        f"{platform} publish HTTP:",
        response.status_code
    )
    print(
        f"{platform} publish response:",
        response.text
    )

    if not response.ok:
        raise RuntimeError(
            f"Status 200 {platform} publishing failed: "
            + response.text
        )

    try:
        result=response.json()
    except Exception as e:
        raise RuntimeError(
            f"Status 200 {platform} returned invalid JSON: {e}"
        )

    return result

# ============================================================
# PUBLISH ONE PLATFORM THROUGH STATUS 200
# ============================================================

def publish_one_status200(
    platform,
    video_path,
    caption,
    api_key,
    account_id
):
    if not api_key:
        raise RuntimeError(
            f"Status 200 {platform} API key is missing."
        )

    if not account_id:
        raise RuntimeError(
            f"Status 200 {platform} account ID is missing."
        )

    if not video_path:
        raise ValueError(
            f"No video path provided for {platform}."
        )

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video file does not exist: {video_path}"
        )

    video_url=get_public_video_url(video_path)

    print()
    print("="*60)
    print(
        f"PROMPTPROHUB STATUS 200 → {platform.upper()}"
    )
    print("="*60)
    print("Platform:",platform)
    print("Status 200 account:",account_id)
    print("Public video URL:",video_url)

    # Check that the Status 200 key sees the account.
    check_status200_account(
        api_key,
        account_id,
        platform
    )

    # Each Status 200 API key gets its own media upload.
    file_id=upload_media_status200(
        video_url,
        api_key,
        platform
    )

    result=create_status200_post(
        platform,
        account_id,
        api_key,
        file_id,
        caption
    )

    print()
    print("="*60)
    print(
        f"STATUS 200 → {platform.upper()} SUCCESS"
    )
    print("="*60)
    print("Account:",account_id)
    print("Result:",result)
    print("="*60)

    return result

# ============================================================
# TIKTOK
# ============================================================

def publish_tiktok_status200(
    video_path,
    caption
):
    return publish_one_status200(
        "tiktok",
        video_path,
        caption,
        STATUS200_TIKTOK_API_KEY,
        STATUS200_TIKTOK_ACCOUNT
    )

# ============================================================
# INSTAGRAM
# ============================================================

def publish_instagram_status200(
    video_path,
    caption
):
    return publish_one_status200(
        "instagram",
        video_path,
        caption,
        STATUS200_INSTAGRAM_API_KEY,
        STATUS200_INSTAGRAM_ACCOUNT
    )

# ============================================================
# YOUTUBE
# ============================================================

def publish_youtube_status200(
    video_path,
    caption
):
    return publish_one_status200(
        "youtube",
        video_path,
        caption,
        STATUS200_YOUTUBE_API_KEY,
        STATUS200_YOUTUBE_ACCOUNT
    )

# ============================================================
# MAIN FUNCTION
# ============================================================

def publish_to_status200(
    video_path,
    caption
):
    print()
    print("="*60)
    print("PROMPTPROHUB STATUS 200 SOCIAL PUBLISHER")
    print("="*60)
    print("TikTok    → STATUS 200")
    print("Instagram → STATUS 200")
    print("YouTube   → STATUS 200")
    print("="*60)

    results={
        "successful":[],
        "failed":[]
    }

    # --------------------------------------------------------
    # TIKTOK
    # --------------------------------------------------------

    try:
        result=publish_tiktok_status200(
            video_path,
            caption
        )
        results["successful"].append({
            "platform":"tiktok",
            "provider":"status200",
            "account":STATUS200_TIKTOK_ACCOUNT,
            "result":result
        })
    except Exception as e:
        print(
            "TikTok publishing failed:",
            str(e)
        )
        results["failed"].append({
            "platform":"tiktok",
            "provider":"status200",
            "account":STATUS200_TIKTOK_ACCOUNT,
            "error":str(e)
        })

    # --------------------------------------------------------
    # INSTAGRAM
    # --------------------------------------------------------

    try:
        result=publish_instagram_status200(
            video_path,
            caption
        )
        results["successful"].append({
            "platform":"instagram",
            "provider":"status200",
            "account":STATUS200_INSTAGRAM_ACCOUNT,
            "result":result
        })
    except Exception as e:
        print(
            "Instagram publishing failed:",
            str(e)
        )
        results["failed"].append({
            "platform":"instagram",
            "provider":"status200",
            "account":STATUS200_INSTAGRAM_ACCOUNT,
            "error":str(e)
        })

    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    try:
        result=publish_youtube_status200(
            video_path,
            caption
        )
        results["successful"].append({
            "platform":"youtube",
            "provider":"status200",
            "account":STATUS200_YOUTUBE_ACCOUNT,
            "result":result
        })
    except Exception as e:
        print(
            "YouTube publishing failed:",
            str(e)
        )
        results["failed"].append({
            "platform":"youtube",
            "provider":"status200",
            "account":STATUS200_YOUTUBE_ACCOUNT,
            "error":str(e)
        })

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    print()
    print("="*60)
    print("STATUS 200 SOCIAL PUBLISHING SUMMARY")
    print("="*60)
    print(
        "Successful:",
        len(results["successful"])
    )
    print(
        "Failed:",
        len(results["failed"])
    )

    for item in results["successful"]:
        print(
            "SUCCESS:",
            item
        )

    for item in results["failed"]:
        print(
            "FAILED:",
            item
        )

    print("="*60)

    return results

# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

def publish_to_tiktok(
    video_path,
    caption
):
    return publish_tiktok_status200(
        video_path,
        caption
    )

# ============================================================
# CONFIGURATION TEST
# ============================================================

if __name__=="__main__":
    print("="*60)
    print(
        "PROMPTPROHUB STATUS 200 CONFIGURATION"
    )
    print("="*60)

    print(
        "STATUS200_TIKTOK_API_KEY:",
        "SET" if STATUS200_TIKTOK_API_KEY else "MISSING"
    )
    print(
        "STATUS200_TIKTOK_ACCOUNT:",
        STATUS200_TIKTOK_ACCOUNT
        if STATUS200_TIKTOK_ACCOUNT
        else "MISSING"
    )

    print(
        "STATUS200_INSTAGRAM_API_KEY:",
        "SET" if STATUS200_INSTAGRAM_API_KEY else "MISSING"
    )
    print(
        "STATUS200_INSTAGRAM_ACCOUNT:",
        STATUS200_INSTAGRAM_ACCOUNT
        if STATUS200_INSTAGRAM_ACCOUNT
        else "MISSING"
    )

    print(
        "STATUS200_YOUTUBE_API_KEY:",
        "SET" if STATUS200_YOUTUBE_API_KEY else "MISSING"
    )
    print(
        "STATUS200_YOUTUBE_ACCOUNT:",
        STATUS200_YOUTUBE_ACCOUNT
        if STATUS200_YOUTUBE_ACCOUNT
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

    print("="*60)
