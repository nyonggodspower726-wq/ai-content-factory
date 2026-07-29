from moviepy.editor import TextClip, CompositeVideoClip


def add_hook(video, text):

    print("Adding hook text...")

    hook = TextClip(
        text,
        fontsize=70,
        color="white",
        method="caption",
        size=(700, None)
    )

    hook = hook.set_duration(3)

    hook = hook.set_position(
        ("center", "top")
    )

    final = CompositeVideoClip(
        [video, hook]
    )

    return final
