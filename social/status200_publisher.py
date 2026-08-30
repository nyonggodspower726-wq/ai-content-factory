import os
import requests
STATUS200_BASE_URL="https://app.status200uploads.com/functions/v1"
STATUS200_API_KEY=os.getenv("STATUS200_API_KEY_1") or os.getenv("STATUS200_API_KEY")
STATUS200_ACCOUNT=os.getenv("STATUS200_ACCOUNT_1") or os.getenv("STATUS200_TIKTOK_ACCOUNT")
STATUS200_PLATFORM="tiktok"
ZERNIO_BASE_URL="https://zernio.com/api/v1"
ZERNIO_API_KEY=os.getenv("ZERNIO_API_KEY") or os.getenv("ZERNIO_API_KEY_1")
ZERNIO_INSTAGRAM_ACCOUNT=os.getenv("ZERNIO_INSTAGRAM_ACCOUNT_ID") or os.getenv("ZERNIO_INSTAGRAM_ACCOUNT") or os.getenv("INSTAGRAM_ACCOUNT_ID")
ZERNIO_YOUTUBE_ACCOUNT=os.getenv("ZERNIO_YOUTUBE_ACCOUNT_ID") or os.getenv("ZERNIO_YOUTUBE_ACCOUNT") or os.getenv("YOUTUBE_ACCOUNT_ID")
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

def get_zernio_headers():
    if not ZERNIO_API_KEY:
        raise RuntimeError("ZERNIO_API_KEY is missing from Railway Variables.")
    return {
        "Authorization":f"Bearer {ZERNIO_API_KEY}",
        "Content-Type":"application/json",
        "Accept":"application/json"
    }

def publish_tiktok_status200(video_path,caption):
    print("="*60)
    print("PROMPTPROHUB STATUS 200 -> TIKTOK")
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
    headers=get_status200_headers()
    print("TikTok account:",STATUS200_ACCOUNT)
    print("Public video URL:",video_url)
    upload_url=f"{STATUS200_BASE_URL}/api-media-upload"
    upload_payload={"url":video_url}
    upload_response=requests.post(upload_url,headers=headers,json=upload_payload,timeout=120)
    print("Status 200 media HTTP:",upload_response.status_code)
    print("Status 200 media response:",upload_response.text)
    if not upload_response.ok:
        raise RuntimeError("Status 200 media upload failed: "+upload_response.text)
    try:
        upload_data=upload_response.json()
    except Exception as e:
        raise RuntimeError(f"Status 200 returned invalid media JSON: {e}")
    file_id=upload_data.get("file_id") or upload_data.get("mediaID") or upload_data.get("mediaId") or upload_data.get("id")
    if not file_id:
        raise RuntimeError("Status 200 media upload succeeded but no media/file ID was returned.\n"+f"Response: {upload_data}")
    print("Status 200 media ID:",file_id)
    post_data={
        "accountId":STATUS200_ACCOUNT,
        "platform":"tiktok",
        "content":{
            "text":str(caption or "").strip(),
            "mediaID":[file_id]
        },
        "tiktok":{
            "privacyLevel":"PUBLIC_TO_EVERYONE"
        }
    }
    publish_payload={"post":post_data}
    publish_url=f"{STATUS200_BASE_URL}/api-posts"
    publish_response=requests.post(publish_url,headers=headers,json=publish_payload,timeout=120)
    print("TikTok publish HTTP:",publish_response.status_code)
    print("TikTok publish response:",publish_response.text)
    if not publish_response.ok:
        raise RuntimeError("Status 200 TikTok publishing failed: "+publish_response.text)
    try:
        result=publish_response.json()
    except Exception as e:
        raise RuntimeError(f"Status 200 returned invalid TikTok JSON: {e}")
    print("="*60)
    print("STATUS 200 -> TIKTOK SUCCESS")
    print("="*60)
    return result

def publish_zernio(video_path,caption):
    print("="*60)
    print("PROMPTPROHUB ZERNIO -> INSTAGRAM + YOUTUBE")
    print("="*60)
    if not ZERNIO_API_KEY:
        raise RuntimeError("ZERNIO_API_KEY is missing from Railway Variables.")
    if not ZERNIO_INSTAGRAM_ACCOUNT:
        raise RuntimeError("ZERNIO Instagram account ID is missing from Railway Variables.")
    if not ZERNIO_YOUTUBE_ACCOUNT:
        raise RuntimeError("ZERNIO YouTube account ID is missing from Railway Variables.")
    if not video_path:
        raise ValueError("No video path provided.")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file does not exist: {video_path}")
    video_url=get_public_video_url(video_path)
    headers=get_zernio_headers()
    print("Instagram Zernio account:",ZERNIO_INSTAGRAM_ACCOUNT)
    print("YouTube Zernio account:",ZERNIO_YOUTUBE_ACCOUNT)
    print("Public video URL:",video_url)
    payload={
        "content":str(caption or "").strip(),
        "mediaItems":[
            {
                "type":"video",
                "url":video_url
            }
        ],
        "platforms":[
            {
                "platform":"instagram",
                "accountId":ZERNIO_INSTAGRAM_ACCOUNT
            },
            {
                "platform":"youtube",
                "accountId":ZERNIO_YOUTUBE_ACCOUNT,
                "platformSpecificData":{
                    "title":str(caption or "").strip()[:100],
                    "visibility":"public"
                }
            }
        ],
        "publishNow":True
    }
    post_url=f"{ZERNIO_BASE_URL}/posts"
    print("Zernio endpoint:",post_url)
    response=requests.post(post_url,headers=headers,json=payload,timeout=180)
    print("Zernio HTTP status:",response.status_code)
    print("Zernio response:",response.text)
    if not response.ok:
        raise RuntimeError("Zernio Instagram/YouTube publishing failed: "+response.text)
    try:
        result=response.json()
    except Exception as e:
        raise RuntimeError(f"Zernio returned invalid JSON: {e}")
    print("="*60)
    print("ZERNIO -> INSTAGRAM + YOUTUBE SUCCESS")
    print("="*60)
    return result

def publish_to_status200(video_path,caption):
    print()
    print("="*60)
    print("PROMPTPROHUB SOCIAL PUBLISHER")
    print("="*60)
    print("TikTok    -> STATUS 200")
    print("Instagram -> ZERNIO")
    print("YouTube   -> ZERNIO")
    print("="*60)
    results={"successful":[],"failed":[]}
    try:
        result=publish_tiktok_status200(video_path,caption)
        results["successful"].append({
            "platform":"tiktok",
            "provider":"status200",
            "result":result
        })
    except Exception as e:
        print("TikTok publishing failed:",str(e))
        results["failed"].append({
            "platform":"tiktok",
            "provider":"status200",
            "error":str(e)
        })
    try:
        result=publish_zernio(video_path,caption)
        results["successful"].append({
            "platforms":["instagram","youtube"],
            "provider":"zernio",
            "result":result
        })
    except Exception as e:
        print("Zernio publishing failed:",str(e))
        results["failed"].append({
            "platforms":["instagram","youtube"],
            "provider":"zernio",
            "error":str(e)
        })
    print()
    print("="*60)
    print("SOCIAL PUBLISHING SUMMARY")
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
    return publish_tiktok_status200(video_path,caption)

if __name__=="__main__":
    print("="*60)
    print("PROMPTPROHUB SOCIAL PUBLISHER CONFIGURATION")
    print("="*60)
    print("STATUS200_API_KEY_1:","SET" if STATUS200_API_KEY else "MISSING")
    print("STATUS200_ACCOUNT_1:",STATUS200_ACCOUNT if STATUS200_ACCOUNT else "MISSING")
    print("ZERNIO_API_KEY:","SET" if ZERNIO_API_KEY else "MISSING")
    print("ZERNIO_INSTAGRAM_ACCOUNT_ID:",ZERNIO_INSTAGRAM_ACCOUNT if ZERNIO_INSTAGRAM_ACCOUNT else "MISSING")
    print("ZERNIO_YOUTUBE_ACCOUNT_ID:",ZERNIO_YOUTUBE_ACCOUNT if ZERNIO_YOUTUBE_ACCOUNT else "MISSING")
    print("RAILWAY_PUBLIC_DOMAIN:",RAILWAY_PUBLIC_DOMAIN if RAILWAY_PUBLIC_DOMAIN else "MISSING")
    print("RAILWAY_PUBLIC_URL:",RAILWAY_PUBLIC_URL if RAILWAY_PUBLIC_URL else "MISSING")
    print("="*60)
