import requests

def download_background():

    url = "https://samplelib.com/lib/preview/mp4/sample-5s.mp4"

    r = requests.get(url)

    with open("background.mp4", "wb") as f:
        f.write(r.content)

    return "background.mp4"
