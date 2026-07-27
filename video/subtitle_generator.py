from moviepy.editor import *


def create_subtitles(script):

    print("Generating subtitles...")

    subtitle = TextClip(
        script,
        fontsize=55,
        color="white",
        method="caption",
        size=(900, None)
    ).set_duration(30)

    subtitle = subtitle.set_position(("center", "bottom"))

    return subtitle
