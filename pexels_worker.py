import os,json,time,requests
PEXELS_API_KEY=os.getenv("PEXELS_API_KEY")
PEXELS_URL="https://api.pexels.com/videos/search"
HISTORY_FILE="data/pexels_video_history.json"
VIDEO_COOLDOWN=300
HISTORY_LIMIT=1000
RESULTS_PER_PAGE=40
MAX_SEARCH_PAGES=10

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
    except:
        return []

def save_history(history):
    ensure_history_dir()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as f:
            json.dump(history[-HISTORY_LIMIT:],f,indent=2)
    except Exception as e:
        print("HISTORY SAVE ERROR:",e)

def normalize_history(history):
    clean=[]
    seen=set()
    for x in history:
        if not isinstance(x,dict): continue
        i=str(x.get("id"))
        if i in seen: continue
        seen.add(i)
        clean.append(x)
    return clean[-HISTORY_LIMIT:]

def recent_ids(history):
    return {str(x.get("id")) for x in history[-VIDEO_COOLDOWN:]}

def record_video(history,video):
    history.append({"id":str(video.get("id")),"time":time.time()})
    history=normalize_history(history)
    save_history(history)
    return history

def search_videos(prompt,page):
    headers={"Authorization":PEXELS_API_KEY}
    params={
        "query":prompt,
        "per_page":RESULTS_PER_PAGE,
        "page":page
    }

    r=requests.get(
        PEXELS_URL,
        headers=headers,
        params=params,
        timeout=60
    )

    print("="*40)
    print("PEXELS STATUS:",r.status_code)
    if r.status_code!=200:
        print(r.text[:300])
    print("="*40)

    r.raise_for_status()
    return r.json()

def choose_fresh_videos(prompt,history):
    used=recent_ids(history)
    fresh=[]

    for page in range(1,MAX_SEARCH_PAGES+1):
        try:
            print("PEXELS PAGE",page)
            data=search_videos(prompt,page)

            for video in data.get("videos",[]):
                vid=str(video.get("id"))

                if vid in used:
                    continue

                files=video.get("video_files",[])
                usable=[x for x in files if x.get("link")]

                if usable:
                    best=max(
                        usable,
                        key=lambda x:x.get("width",0)*x.get("height",0)
                    )

                    fresh.append({
                        "id":vid,
                        "url":best["link"]
                    })

        except Exception as e:
            print("PEXELS PAGE ERROR:",e)

    return fresh

def generate_pexels_video(prompt):
    if not PEXELS_API_KEY:
        print("PEXELS KEY MISSING")
        return None

    try:
        history=normalize_history(load_history())

        videos=choose_fresh_videos(
            prompt,
            history
        )

        if not videos:
            print("NO FRESH VIDEO FOUND")
            return None

        selected=videos[0]

        record_video(
            history,
            {"id":selected["id"]}
        )

        print("="*50)
        print("PEXELS VIDEO READY")
        print("ID:",selected["id"])
        print("AVAILABLE:",len(videos))
        print("="*50)

        return videos

    except Exception as e:
        print("PEXELS WORKER FAILED:",e)
        return None
