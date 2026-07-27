import os

def upload_to_youtube(video_path, title, description):

    """
    Upload a YouTube Short.

    Placeholder.
    Later we'll connect it to the YouTube Data API.
    """

    if not os.path.exists(video_path):
        print("Video not found.")
        return False

    print(f"Uploading {video_path} to YouTube Shorts...")
    print(title)
    print(description)

    print("Upload completed.")

    return True
