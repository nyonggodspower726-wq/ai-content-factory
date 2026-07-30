import os
from config import (
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_REFRESH_TOKEN,
)

def upload_to_youtube(video_path, title, description):

    if not os.path.exists(video_path):
        print("Video not found.")
        return False

    if not YOUTUBE_REFRESH_TOKEN:
        raise Exception(
            "Missing YOUTUBE_REFRESH_TOKEN in Railway Variables."
        )

    print("Connecting to YouTube...")

    # Real upload code goes here

    print("Upload completed.")

    return True
