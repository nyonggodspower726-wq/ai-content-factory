import os
import requests

STATUS200_BASE_URL="https://app.status200uploads.com/functions/v1"
STATUS200_API_KEY=os.getenv("STATUS200_API_KEY_1") or os.getenv("STATUS200_API_KEY")
STATUS200_ACCOUNT=os.getenv("STATUS200_ACCOUNT_1") or os.getenv("STATUS200_TIKTOK_ACCOUNT")
STATUS200_PLATFORM="tiktok"

STATUS200_INSTAGRAM_ACCOUNT=os.getenv("STATUS200_INSTAGRAM_ACCOUNT_1") or os.getenv("STATUS200_INSTAGRAM_ACCOUNT")
STATUS200_YOUTUBE_ACCOUNT=os.getenv("STATUS200_YOUTUBE_ACCOUNT_1") or os.getenv("STATUS200_YOUTUBE_ACCOUNT")

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
    raise RuntimeError("Railway public URL is missing. Configure RAILWAY_PUBLIC_DOMAIN or RAILWAY_PUBLIC_URL.")

def get_public_video_url(video_path):
    if not video_path:
        raise ValueError("No video path was provided.")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")
    filename=os.path.basename(video_path)
    return f"{get_railway_public_url()}/videos/{filename}"

def get_status200_headers():
    if not STATUS200_API_KEY:
        raise RuntimeError("STATUS200_API_KEY_1 is missing from Railway Variables.")
    return {
        "Authorization":f"Bearer {STATUS200_API_KEY}",
        "Content-Type":"application/json",
        "Accept":"application/json"
    }

def get_status200_profiles():
    headers=get_status200_headers()
    url=f"{STATUS200_BASE_URL}/api-posts"
    response=requests.get(
        url,
        headers=headers,
        params={"action":"profiles"},
        timeout=60
    )
    print("Status 200 profiles HTTP:",response.status_code)
    print("Status 200 profiles response:",response.text)
    if not response.ok:
        raise RuntimeError("Unable to retrieve Status 200 profiles: "+response.text)
    try:
        data=response.json()
    except Exception as e:
        raise RuntimeError(f"Status 200 returned invalid profiles JSON: {e}")
    return data.get("profiles",[])

def find_status200_account(platform,configured_account=None):
    if configured_account:
        return configured_account.strip()
    profiles=get_status200_profiles()
    for profile in profiles:
        if str(profile.get("platform","")).lower()==platform.lower() and str(profile.get("status","")).lower()=="active":
            account_id=profile.get("account_id") or profile.get("accountId")
            if account_id:
                return account_id
    raise RuntimeError(f"No active Status 200 {platform} account was found. Connect {platform} in Status 200 or configure its Railway account variable.")

def upload_media_to_status200(video_url):
    headers=get_status200_headers()
    upload_url=f"{STATUS200_BASE_URL}/api-media-upload"
    upload_payload={"url":video_url}
    print("-"*60)
    print("STATUS 200 MEDIA UPLOAD")
    print("-"*60)
    print("Media URL:",video_url)
    response=requests.post(
        upload_url,
        headers=headers,
        json=upload_payload,
        timeout=120
    )
    print("Media upload HTTP:",response.status_code)
    print("Media upload response:",response.text)
    if not response.ok:
        raise RuntimeError("Status 200 media upload failed: "+response.text)
    try:
        data=response.json()
    except Exception as e:
        raise RuntimeError(f"Status 200 returned invalid media JSON: {e}")
    file_id=(
        data.get("file_id")
        or data.get("mediaID")
        or data.get("mediaId")
        or data.get("id")
    )
    if not file_id:
        raise RuntimeError(
            "Status 200 media upload succeeded but no media/file ID was returned.\n"
            f"Response: {data}"
        )
    print("Status 200 media ID:",file_id)
    return file_id

def publish_status200_platform(platform,account_id,file_id,caption):
    headers=get_status200_headers()
    text=str(caption or "").strip()
    post_data={
        "accountId":account_id,
        "platform":platform,
        "content":{
            "text":text,
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
            "privacy":"public"
        }
    publish_url=f"{STATUS200_BASE_URL}/api-posts"
    print("-"*60)
    print(f"STATUS 200 → {platform.upper()}")
    print("-"*60)
    print("Account:",account_id)
    print("Media ID:",file_id)
    print("Endpoint:",publish_url)
    response=requests.post(
        publish_url,
        headers=headers,
        json={"post":post_data},
        timeout=180
    )
    print(f"{platform.upper()} HTTP:",response.status_code)
    print(f"{platform.upper()} response:",response.text)
    if not response.ok:
        raise RuntimeError(
            f"Status 200 {platform} publishing failed: {response.text}"
        )
    try:
        result=response.json()
    except Exception as e:
        raise RuntimeError(
            f"Status 200 returned invalid {platform} JSON: {e}"
        )
    return result

def publish_to_status200(video_path,caption):
    print()
    print("="*60)
    print("PROMPTPROHUB STATUS 200 SOCIAL PUBLISHER")
    print("="*60)
    print("TikTok    → STATUS 200")
    print("Instagram → STATUS 200")
    print("YouTube   → STATUS 200")
    print("="*60)

    if not STATUS200_API_KEY:
        raise RuntimeError("STATUS200_API_KEY_1 is missing from Railway Variables.")

    if not STATUS200_ACCOUNT:
        raise RuntimeError("STATUS200_ACCOUNT_1 is missing from Railway Variables.")

    if not video_path:
        raise ValueError("No video path provided.")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist: {video_path}")

    video_url=get_public_video_url(video_path)

    print("Local video:",video_path)
    print("Public video URL:",video_url)

    file_id=upload_media_to_status200(video_url)

    results={
        "successful":[],
        "failed":[]
    }

    try:
        result=publish_status200_platform(
            "tiktok",
            STATUS200_ACCOUNT,
            file_id,
            caption
        )
        results["successful"].append({
            "platform":"tiktok",
            "account":STATUS200_ACCOUNT,
            "result":result
        })
    except Exception as e:
        print("TikTok publishing failed:",str(e))
        results["failed"].append({
            "platform":"tiktok",
            "account":STATUS200_ACCOUNT,
            "error":str(e)
        })

    try:
        instagram_account=find_status200_account(
            "instagram",
            STATUS200_INSTAGRAM_ACCOUNT
        )
        result=publish_status200_platform(
            "instagram",
            instagram_account,
            file_id,
            caption
        )
        results["successful"].append({
            "platform":"instagram",
            "account":instagram_account,
            "result":result
        })
    except Exception as e:
        print("Instagram publishing failed:",str(e))
        results["failed"].append({
            "platform":"instagram",
            "error":str(e)
        })

    try:
        youtube_account=find_status200_account(
            "youtube",
            STATUS200_YOUTUBE_ACCOUNT
        )
        result=publish_status200_platform(
            "youtube",
            youtube_account,
            file_id,
            caption
        )
        results["successful"].append({
            "platform":"youtube",
            "account":youtube_account,
            "result":result
        })
    except Exception as e:
        print("YouTube publishing failed:",str(e))
        results["failed"].append({
            "platform":"youtube",
            "error":str(e)
        })

    print()
    print("="*60)
    print("STATUS 200 SOCIAL PUBLISHING SUMMARY")
    print("="*60)
    print("Successful:",len(results["successful"]))
    print("Failed:",len(results["failed"]))

    for item in results["successful"]:
        print("SUCCESS:",item)

    for item in results["failed"]:
        print("FAILED:",item)

    print("="*60)

    return results

def publish_to_tiktok(video_path,caption):
    return publish_status200_platform(
        "tiktok",
        STATUS200_ACCOUNT,
        upload_media_to_status200(get_public_video_url(video_path)),
        caption
    )

if __name__=="__main__":
    print("="*60)
    print("PROMPTPROHUB STATUS 200 CONFIGURATION")
    print("="*60)
    print("STATUS200_API_KEY_1:","SET" if STATUS200_API_KEY else "MISSING")
    print("STATUS200_ACCOUNT_1:",STATUS200_ACCOUNT if STATUS200_ACCOUNT else "MISSING")
    print("STATUS200_INSTAGRAM_ACCOUNT_1:",STATUS200_INSTAGRAM_ACCOUNT if STATUS200_INSTAGRAM_ACCOUNT else "AUTO-DISCOVERY")
    print("STATUS200_YOUTUBE_ACCOUNT_1:",STATUS200_YOUTUBE_ACCOUNT if STATUS200_YOUTUBE_ACCOUNT else "AUTO-DISCOVERY")
    print("RAILWAY_PUBLIC_DOMAIN:",RAILWAY_PUBLIC_DOMAIN if RAILWAY_PUBLIC_DOMAIN else "MISSING")
    print("RAILWAY_PUBLIC_URL:",RAILWAY_PUBLIC_URL if RAILWAY_PUBLIC_URL else "MISSING")
    print("="*60)
