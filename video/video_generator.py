from video.background_video import download_background

def create_video():

    print("Creating AI video...")

    background = download_background()

    print(f"Background video downloaded: {background}")

    return background
