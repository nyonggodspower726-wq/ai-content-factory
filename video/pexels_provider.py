import os,json,time,requests

PEXELS_API_KEY=os.getenv("PEXELS_API_KEY")
PEXELS_URL="https://api.pexels.com/v1/search"
HISTORY_FILE="data/pexels_image_history.json"

IMAGE_COOLDOWN=300
HISTORY_LIMIT=1000
RESULTS_PER_PAGE=80
MAX_SEARCH_PAGES=10

def ensure_history_directory():
    d=os.path.dirname(HISTORY_FILE)
    if d:
        os.makedirs(d,exist_ok=True)

def load_history():
    ensure_history_directory()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
        return data if isinstance(data,list) else []
    except Exception as e:
        print("IMAGE HISTORY LOAD ERROR:",e)
        return []

def save_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as f:
            json.dump(history[-HISTORY_LIMIT:],f,indent=2,ensure_ascii=False)
    except Exception as e:
        print("IMAGE HISTORY SAVE ERROR:",e)

def normalize_history(history):
    clean=[]
    seen=set()
    for item in history:
        if not isinstance(item,dict):
            continue
        pid=str(item.get("id"))
        if pid in seen:
            continue
        seen.add(pid)
        clean.append(item)
    return clean[-HISTORY_LIMIT:]

def get_recent_ids(history):
    return {
        str(x.get("id"))
        for x in history[-IMAGE_COOLDOWN:]
        if isinstance(x,dict)
    }

def record_image(history,photo):
    history.append({
        "id":str(photo.get("id")),
        "source":"pexels",
        "time":time.time()
    })
    history=normalize_history(history)
    save_history(history)
    return history

def search_images(prompt,page):
    headers={
        "Authorization":PEXELS_API_KEY
    }

    params={
        "query":prompt,
        "per_page":RESULTS_PER_PAGE,
        "page":page,
        "orientation":"portrait"
    }

    r=requests.get(
        PEXELS_URL,
        headers=headers,
        params=params,
        timeout=60
    )

    print("="*50)
    print("PEXELS IMAGE STATUS:",r.status_code)

    if r.status_code!=200:
        print(r.text[:500])

    print("="*50)

    r.raise_for_status()

    return r.json()

def choose_fresh_photo(prompt,history):

    used=get_recent_ids(history)

    photos=[]

    for page in range(1,MAX_SEARCH_PAGES+1):

        try:

            print("PEXELS IMAGE PAGE:",page)

            data=search_images(
                prompt,
                page
            )

            results=data.get("photos",[])

            for photo in results:

                pid=str(photo.get("id"))

                if pid in used:
                    continue

                photos.append(photo)

        except Exception as e:

            print("PEXELS PAGE ERROR:",e)

    if not photos:
        return None

    return photos[0]

def download_image(url,path):

    r=requests.get(
        url,
        timeout=60
    )

    r.raise_for_status()

    with open(path,"wb") as f:
        f.write(r.content)

    return path

def build_filename(prompt,pid):

    name="".join(
        c if c.isalnum() else "_"
        for c in prompt[:50]
    )

    return f"{name}_{pid}.jpg"

def generate_ai_image(prompt,output_folder="assets/images"):

    if not PEXELS_API_KEY:
        print("PEXELS KEY MISSING")
        return None

    try:

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        history=normalize_history(
            load_history()
        )

        photo=choose_fresh_photo(
            prompt,
            history
        )

        if not photo:

            print("NO FRESH IMAGE AVAILABLE")

            return None


        pid=str(photo.get("id"))

        url=photo.get(
            "src",
            {}
        ).get(
            "large2x"
        )

        if not url:

            url=photo.get(
                "src",
                {}
            ).get(
                "large"
            )

        if not url:

            print("NO IMAGE URL")

            return None


        filename=build_filename(
            prompt,
            pid
        )

        path=os.path.join(
            output_folder,
            filename
        )


        if not os.path.exists(path):

            download_image(
                url,
                path
            )


        if os.path.getsize(path)<=0:

            return None


        record_image(
            history,
            photo
        )


        print("="*50)
        print("PEXELS IMAGE READY")
        print("ID:",pid)
        print("COOLDOWN:",IMAGE_COOLDOWN)
        print("="*50)


        return path


    except Exception as e:

        print("="*50)
        print("PEXELS IMAGE FAILED")
        print(type(e).__name__)
        print(e)
        print("="*50)

        return None
