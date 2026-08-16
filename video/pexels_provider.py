import os,json,time,requests
from config import PEXELS_API_KEY

PEXELS_URL="https://api.pexels.com/v1/search"
HISTORY_FILE="data/pexels_image_history.json"

# ============================================================
# 300-ITEM ANTI-REPEAT SYSTEM
# ============================================================
IMAGE_COOLDOWN=300
HISTORY_LIMIT=1000
SEARCH_RESULTS_PER_PAGE=20
MAX_SEARCH_PAGES=20

def ensure_history_directory():
    directory=os.path.dirname(HISTORY_FILE)
    if directory:
        os.makedirs(directory,exist_ok=True)

def load_history():
    ensure_history_directory()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
        if not isinstance(data,list):
            return []
        return data
    except Exception as e:
        print("="*60)
        print("PEXELS HISTORY LOAD ERROR")
        print("="*60)
        print(e)
        print("="*60)
        return []

def save_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as f:
            json.dump(history[-HISTORY_LIMIT:],f,indent=2,ensure_ascii=False)
    except Exception as e:
        print("="*60)
        print("PEXELS HISTORY SAVE ERROR")
        print("="*60)
        print(e)
        print("="*60)

def normalize_history(history):
    cleaned=[]
    seen=set()
    for item in history:
        if not isinstance(item,dict):
            continue
        photo_id=item.get("id")
        if photo_id is None:
            continue
        photo_id=str(photo_id)
        if photo_id in seen:
            continue
        seen.add(photo_id)
        cleaned.append(item)
    return cleaned[-HISTORY_LIMIT:]

def get_recent_ids(history):
    recent=history[-IMAGE_COOLDOWN:]
    return {str(item.get("id")) for item in recent if item.get("id") is not None}

def record_image_usage(history,photo):
    item={
        "id":str(photo.get("id")),
        "photographer":photo.get("photographer",""),
        "source":"pexels",
        "timestamp":int(time.time())
    }
    history.append(item)
    history=normalize_history(history)
    save_history(history)
    return history

def download_image(url,output_path):
    response=requests.get(url,timeout=60)
    response.raise_for_status()
    with open(output_path,"wb") as f:
        f.write(response.content)
    return output_path

def build_filename(prompt,photo_id):
    safe_prompt="".join(c if c.isalnum() else "_" for c in prompt[:60]).strip("_").lower()
    if not safe_prompt:
        safe_prompt="pexels"
    return f"{safe_prompt}_{photo_id}.jpg"

def search_pexels(prompt,page):
    headers={"Authorization":PEXELS_API_KEY}
    params={
        "query":prompt,
        "per_page":SEARCH_RESULTS_PER_PAGE,
        "page":page,
        "orientation":"portrait"
    }
    response=requests.get(PEXELS_URL,headers=headers,params=params,timeout=60)
    response.raise_for_status()
    return response.json()

def choose_fresh_photo(prompt,history):
    recent_ids=get_recent_ids(history)
    print("="*60)
    print("PEXELS IMAGE SEARCH")
    print("="*60)
    print("Searching:",prompt)
    print("Anti-repeat cooldown:",IMAGE_COOLDOWN)
    print("Search pages:",MAX_SEARCH_PAGES)
    print("Results per page:",SEARCH_RESULTS_PER_PAGE)
    print("Protected recent IDs:",len(recent_ids))
    print("="*60)

    for page in range(1,MAX_SEARCH_PAGES+1):
        try:
            print(f"Searching Pexels page {page}/{MAX_SEARCH_PAGES}...")
            data=search_pexels(prompt,page)
            photos=data.get("photos",[])
            if not photos:
                print("No results on page:",page)
                continue

            fresh_photos=[
                photo for photo in photos
                if str(photo.get("id")) not in recent_ids
            ]

            print("Results:",len(photos))
            print("Fresh results:",len(fresh_photos))

            if fresh_photos:
                selected=fresh_photos[0]
                print("Fresh Pexels photo selected:",selected.get("id"))
                return selected

        except Exception as e:
            print("PEXELS SEARCH PAGE ERROR:",page,e)
            continue

    print("="*60)
    print("NO FRESH PEXELS IMAGE FOUND")
    print("="*60)
    print(f"Pexels could not provide an unused image outside the last {IMAGE_COOLDOWN} images.")
    print("IMPORTANT: No old image will be intentionally reused.")
    print("="*60)
    return None

def generate_ai_image(prompt,output_folder="assets/images"):
    os.makedirs(output_folder,exist_ok=True)
    history=normalize_history(load_history())

    try:
        photo=choose_fresh_photo(prompt,history)

        if not photo:
            print("No fresh Pexels image available.")
            print("Video generation stopped instead of reusing a recent image.")
            return None

        photo_id=str(photo.get("id"))

        image_url=photo.get("src",{}).get("large2x")
        if not image_url:
            image_url=photo.get("src",{}).get("large")

        if not image_url:
            print("Pexels photo has no usable image URL.")
            return None

        photographer=photo.get("photographer","")

        print("="*60)
        print("SELECTED PEXELS PHOTO")
        print("="*60)
        print("Photo ID:",photo_id)
        print("Photographer:",photographer)
        print("="*60)

        filename=build_filename(prompt,photo_id)
        image_path=os.path.join(output_folder,filename)

        if os.path.exists(image_path):
            print("Using existing downloaded image:",image_path)
        else:
            print("Downloading:",image_url)
            download_image(image_url,image_path)
            print("Downloaded:",image_path)

        if not os.path.exists(image_path):
            print("Downloaded image is missing.")
            return None

        file_size=os.path.getsize(image_path)

        if file_size<=0:
            print("Downloaded image is empty.")
            return None

        history=record_image_usage(history,photo)

        print("="*60)
        print("PEXELS IMAGE READY")
        print("="*60)
        print("Photo ID:",photo_id)
        print("File:",image_path)
        print("Cooldown:",f"{IMAGE_COOLDOWN} videos")
        print("History size:",len(history))
        print("Status: FRESH IMAGE")
        print("="*60)

        return image_path

    except Exception as e:
        print("="*60)
        print("PEXELS FAILED")
        print("="*60)
        print(type(e).__name__)
        print(e)
        print("="*60)
        return None
