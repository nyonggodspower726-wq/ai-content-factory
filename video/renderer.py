import os

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


class Renderer:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB IMAGE RENDER ENGINE")
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

            path = scene.get("image")

            if not path:

                continue

            if not os.path.exists(path):

                continue

            try:

                duration = scene.get(
                    "duration",
                    5
                )

                clip = (

                    ImageClip(path)

                    .set_duration(duration)

                    .resize(height=1280)

                    .crop(
                        x_center=360,
                        y_center=640,
                        width=720,
                        height=1280
                    )

                )

                # ====================================
                # Simple Cinematic Motion
                # ====================================

                motion = scene.get(
                    "motion",
                    "slow_zoom"
                )

                if motion == "slow_zoom":

                    clip = clip.resize(
                        lambda t: 1 + (
                            0.05 * t / duration
                        )
                    )

                elif motion == "zoom_out":

                    clip = clip.resize(
                        lambda t: 1.05 - (
                            0.05 * t / duration
                        )
                    )

                clip = clip.fadein(0.5)

                clip = clip.fadeout(0.5)

                scene["clip_object"] = clip

                clips.append(
                    clip
                )

            except Exception as e:

                print(e)

        if len(clips) == 0:

            print("No images loaded.")

            return None

        final = concatenate_videoclips(

            clips,

            method="compose"

        )

        audio = None

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

        if audio:

            audio.close()

        for clip in clips:

            clip.close()

        final.close()

        print("Rendering completed.")

        return output
