from moviepy.video.fx import all as vfx


def apply_zoom(clip):
    """
    Adds a gentle zoom-in effect.
    """
    return clip.fx(
        vfx.resize,
        lambda t: 1 + (0.05 * t / clip.duration)
    )
