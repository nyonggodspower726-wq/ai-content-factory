import os,json,time,requests
PEXELS_API_KEY=os.getenv("PEXELS_API_KEY")
PEXELS_URL="https://api.pexels.com/videos/search"
HISTORY_FILE="data/pexels_video_history.json"
VIDEO_COOLDOWN=300
HISTORY_LIMIT=1000
RESULTS_PER_PAGE=80
MAX_SEARCH_PAGES=20

def ensure_history_dir():
    d=os.path.dirname(HISTORY_FILE)
    if d: os.makedirs(d,exist_ok=True)

def load_history():
    ensure_history_dir()
    if not os.path.exists(HISTORY_FILE): return []
    try:
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
        return data if isinstance(data,list) else []
    except Exception as e:
        print("PEXELS VIDEO HISTORY LOAD ERROR:",e)
        return []

def save_history(history):
    ensure_history_dir()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as f:
            json.dump(history[-HISTORY_LIMIT:],f,indent=2,ensure_ascii=False)
    except Exception as e:
        print("PEXELS VIDEO HISTORY SAVE ERROR:",e)

def normalize_history(history):
    cleaned=[]
    seen=set()
    for item in history:
        if not isinstance(item,dict): continue
        video_id=item.get("id")
        if video_id is None: continue
        video_id=str(video_id)
        if video_id in seen: continue
        seen.add(video_id)
        cleaned.append(item)
    return cleaned[-HISTORY_LIMIT:]

def get_recent_ids(history):
    return {str(x.get("id")) for x in history[-VIDEO_COOLDOWN:] if isinstance(x,dict) and x.get("id") is not None}

def record_video(history,video):
    video_id=str(video.get("id"))
    history.append({"id":video_id,"source":"pexels","timestamp":int(time.time())})
    history=normalize_history(history)
    save_history(history)
    return history

def search_videos(prompt,page):
    headers={"Authorization":PEXELS_API_KEY}
    params={"query":prompt,"per_page":RESULTS_PER_PAGE,"page":page}
    response=requests.get(PEXELS_URL,headers=headers,params=params,timeout=60)
    response.raise_for_status()
    return response.json()

def choose_fresh_videos(prompt,history):
    recent_ids=get_recent_ids(history)
    print("="*60)
    print("PEXELS VIDEO SEARCH")
    print("="*60)
    print("Query:",prompt)
    print("Protected clips:",len(recent_ids))
    print("Cooldown:",VIDEO_COOLDOWN)
    print("Results per page:",RESULTS_PER_PAGE)
    print("Max pages:",MAX_SEARCH_PAGES)
    print("="*60)
    fresh=[]
    for page in range(1,MAX_SEARCH_PAGES+1):
        try:
            print(f"Searching Pexels video page {page}/{MAX_SEARCH_PAGES}...")
            data=search_videos(prompt,page)
            videos=data.get("videos",[])
            if not videos:
                print("No videos on page:",page)
                continue
            page_fresh=[v for v in videos if str(v.get("id")) not in recent_ids]
            print("Results:",len(videos),"Fresh:",len(page_fresh))
            for video in page_fresh:
                files=video.get("video_files",[])
                if not files: continue
                usable=[f for f in files if f.get("link")]
                if not usable: continue
                best=max(usable,key=lambda x:x.get("width",0)*x.get("height",0))
                fresh.append({"provider":"pexels","url":best["link"],"id":str(video.get("id"))})
        except Exception as e:
            print("PEXELS VIDEO SEARCH ERROR:",e)
            continue
    if not fresh:
        print("="*60)
        print("NO FRESH PEXELS VIDEOS FOUND")
        print("="*60)
        return []
    unique=[]
    seen=set()
    for item in fresh:
        if item["id"] in seen: continue
        seen.add(item["id"])
        unique.append(item)
    return unique

def generate_pexels_video(prompt):
    if not PEXELS_API_KEY:
        print("PEXELS_API_KEY not found")
        return None
    try:
        history=normalize_history(load_history())
        fresh=choose_fresh_videos(prompt,history)
        if not fresh:
            print("No fresh Pexels video available.")
            print("No recent clip will be intentionally reused.")
            return None
        urls=[]
        for item in fresh:
            urls.append({"provider":"pexels","url":item["url"],"id":item["id"]})
        selected=urls[0]
        video_id=selected["id"]
        print("="*60)
        print("FRESH PEXELS VIDEO SELECTED")
        print("="*60)
        print("Video ID:",video_id)
        print("Fresh candidates:",len(urls))
        print("Cooldown:",VIDEO_COOLDOWN)
        print("="*60)
        record_video(history,{"id":video_id})
        return urls
    except Exception as e:
        print("="*60)
        print("PEXELS VIDEO ERROR")
        print("="*60)
        print(type(e).__name__,e)
        print("="*60)
        return None
