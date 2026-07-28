import os

def create_video(script):

    print("Creating AI video...")

    os.makedirs("output", exist_ok=True)

    with open("output/video_script.txt", "w", encoding="utf-8") as f:
        f.write(script)

    print("Video assets prepared.")

    return "output/video_script.txt"
