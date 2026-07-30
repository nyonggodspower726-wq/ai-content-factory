from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip


def add_subtitles(video_file, script):

    print("Creating captions...")

    try:

        video = VideoFileClip(video_file)

        words = script.split()

        if not words:
            return video_file

        subtitles = []

        duration = video.duration

        chunk_size = 8

        total_chunks = max(
            1,
            (len(words) + chunk_size - 1) // chunk_size
        )

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
                .set_position(("center", "bottom"))
            )


            subtitles.append(caption)


        final = CompositeVideoClip(
            [video] + subtitles
        )


        output = "output/subtitled_video.mp4"


        final.write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            preset="ultrafast",
            threads=1,
            logger="bar"
        )


        video.close()
        final.close()


        print("Subtitles completed.")

        return output


    except Exception as e:

        print(f"Subtitle error: {e}")

        return video_file
