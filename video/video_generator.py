from moviepy.editor import *

def create_video():

    print("Creating TikTok video...")

    background = ColorClip(
        size=(1080, 1920),
        color=(20, 20, 20),
        duration=30
    )

    title = TextClip(
        "AI CONTENT FACTORY",
        fontsize=80,
        color="white"
    ).set_duration(30)

    title = title.set_position("center")

    audio = AudioFileClip("output.mp3")

    final_video = CompositeVideoClip(
        [background, title]
    ).set_audio(audio)

    final_video.write_videofile(
        "video.mp4",
        fps=30
    )

    return "video.mp4"
