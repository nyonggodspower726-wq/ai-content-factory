from moviepy.editor import ColorClip

def create_video():

    print("Creating placeholder video...")

    video = ColorClip(
        size=(1080, 1920),
        color=(20, 20, 20),
        duration=30
    )

    video.write_videofile(
        "video.mp4",
        fps=30
    )

    return "video.mp4"
