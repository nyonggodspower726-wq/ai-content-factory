from moviepy.editor import TextClip, CompositeVideoClip


def create_subtitles(video, script):

    print("Creating captions...")

    words = script.split()

    subtitles = []

    duration = video.duration

    chunk_size = 8

    total_chunks = max(1, (len(words) + chunk_size - 1) // chunk_size)

    chunk_duration = duration / total_chunks

    for i in range(total_chunks):

        text = " ".join(
            words[i * chunk_size:(i + 1) * chunk_size]
        )

        caption = (
            TextClip(
                text,
                fontsize=55,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(650, None)
            )
            .set_start(i * chunk_duration)
            .set_duration(chunk_duration)
            .set_position(("center", 1050))
        )

        subtitles.append(caption)

    return CompositeVideoClip(
        [video] + subtitles
    )
