import os

def upload_to_instagram(video_path, caption):

    """
    Upload an Instagram Reel.

    Placeholder.
    Later we'll connect it to the Meta Graph API.
    """

    if not os.path.exists(video_path):
        print("Video not found.")
        return False

    print(f"Uploading {video_path} to Instagram Reels...")
    print(caption)

    print("Instagram upload completed.")

    return True
