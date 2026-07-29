from moviepy.video.fx import all as vfx


def apply_zoom(clip):

    print("Applying zoom effect...")

    return clip.fx(
        vfx.resize,
        lambda t: 1 + (0.05 * t / clip.duration)
    )
