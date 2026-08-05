import os

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    concatenate_videoclips
)


class Renderer:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB RENDER ENGINE")
        print("=" * 60)

        os.makedirs(
            "output",
            exist_ok=True
        )

    def render(

        self,

        timeline,

        voice_file=None

    ):

        if not timeline:

            print("No timeline.")

            return None

        clips = []

        for scene in timeline:

            path = scene.get("clip")

            if not path:

                continue

            if not os.path.exists(path):

                continue

            try:

                clip = VideoFileClip(path)

                clip = clip.resize(

                    height=1280

                )

                clip = clip.crop(

                    x_center=clip.w / 2,

                    y_center=clip.h / 2,

                    width=720,

                    height=1280

                )

                duration = scene.get(

                    "duration",

                    5

                )

                clip = clip.subclip(

                    0,

                    min(

                        duration,

                        clip.duration

                    )

                )

                clips.append(

                    clip

                )

            except Exception as e:

                print(e)

        if len(clips) == 0:

            print("No clips loaded.")

            return None

        final = concatenate_videoclips(

            clips,

            method="compose"

        )

        if (

            voice_file

            and

            os.path.exists(

                voice_file

            )

        ):

            audio = AudioFileClip(

                voice_file

            )

            final = final.set_audio(

                audio

            )

        output = "output/ai_sales_video.mp4"

        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=30,

            preset="medium",

            bitrate="3500k",

            logger=None

        )

        try:

            final.close()

        except Exception:

            pass

        print("Rendering completed.")

        return output
