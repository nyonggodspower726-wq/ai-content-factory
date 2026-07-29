from moviepy.editor import TextClip, CompositeVideoClip


def add_subtitles(video, script):
    """
    Adds simple TikTok-style captions to a MoviePy video.
    """

    words = script.split()

    if not words:
        return video

    words_per_caption = 5
    duration_per_caption = video.duration / max(
        1,
        (len(words) + words_per_caption - 1) // words_per_caption
    )

    clips = []

    start = 0

    for i in range(0, len(words), words_per_caption):

        caption = " ".join(words[i:i + words_per_caption])

        txt = (
            TextClip(
                caption,
                fontsize=60,
                color="white",
                stroke_color="black",
                stroke_width=3,
                method="caption",
                size=(650, None),
                align="center"
            )
            .set_position(("center", "bottom"))
            .set_start(start)
            .set_duration(duration_per_caption)
        )

        clips.append(txt)

        start += duration_per_caption

    return CompositeVideoClip([video] + clips)
