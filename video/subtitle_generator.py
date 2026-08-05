import os

from moviepy.editor import (
    TextClip,
    CompositeVideoClip,
    VideoFileClip
)


def add_subtitles(

    video_file,

    script

):

    print("=" * 60)
    print("PROMPTPROHUB SUBTITLE ENGINE")
    print("=" * 60)

    video = None
    final = None

    try:

        video = VideoFileClip(
            video_file
        )

        # ---------------------------------------
        # Accept JSON script or normal text
        # ---------------------------------------

        if isinstance(script, dict):

            text = script.get(
                "script",
                ""
            )

        else:

            text = str(script)

        words = text.split()

        if len(words) == 0:

            print(
                "No subtitle text found."
            )

            return video_file


        subtitles = []

        duration = video.duration

        chunk_size = 10

        total_chunks = max(

            1,

            (len(words) + chunk_size - 1) // chunk_size

        )

        chunk_duration = duration / total_chunks


        for i in range(total_chunks):

            subtitle_text = " ".join(

                words[

                    i * chunk_size :

                    (i + 1) * chunk_size

                ]

            )


            caption = (

                TextClip(

                    subtitle_text,

                    fontsize=60,

                    color="white",

                    stroke_color="black",

                    stroke_width=3,

                    method="caption",

                    size=(700, None)

                )

                .set_start(

                    i * chunk_duration

                )

                .set_duration(

                    chunk_duration

                )

                .set_position(

                    ("center", 980)

                )

            )


            subtitles.append(
                caption
            )


        final = CompositeVideoClip(

            [

                video

            ] + subtitles

        )


        os.makedirs(

            "output",

            exist_ok=True

        )


        output = "output/subtitled_video.mp4"


        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=video.fps or 30,

            preset="medium",

            threads=4,

            logger=None

        )


        print(
            "Subtitles completed successfully."
        )


        return output


    except Exception as e:

        print("=" * 60)
        print("SUBTITLE ENGINE FAILED")
        print("=" * 60)

        print(e)

        return video_file


    finally:

        try:

            if video:

                video.close()

        except Exception:

            pass


        try:

            if final:

                final.close()

        except Exception:

            pass
