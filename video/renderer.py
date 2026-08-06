import PIL.Image

# =====================================================
# Pillow Compatibility Fix
# =====================================================
if not hasattr(PIL.Image, "ANTIALIAS"):
    try:
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
import gc

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


class Renderer:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB LIGHTWEIGHT RENDER ENGINE")
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

                print(f"Missing image: {path}")

                continue

            try:

                duration = scene.get(
                    "duration",
                    5
                )

                clip = (
                    ImageClip(path)
                    .set_duration(duration)
                    .resize((720, 1280))
                )

                motion = scene.get(
                    "motion",
                    "slow_zoom"
                )

                if motion == "slow_zoom":

                    clip = clip.resize(
                        lambda t: 1 + (
                            0.03 * t / duration
                        )
                    )

                elif motion == "zoom_out":

                    clip = clip.resize(
                        lambda t: 1.03 - (
                            0.03 * t / duration
                        )
                    )

                clip = clip.fadein(0.3)
                clip = clip.fadeout(0.3)

                clips.append(clip)

            except Exception as e:

                print("Renderer Error:", e)

        if not clips:

            print("No images loaded.")

            return None

        try:

            final = concatenate_videoclips(
                clips,
                method="chain"
            )

        except Exception:

            final = concatenate_videoclips(
                clips,
                method="compose"
            )

        audio = None

        if (
            voice_file
            and
            os.path.exists(voice_file)
        ):

            audio = AudioFileClip(
                voice_file
            )

            final = final.set_audio(audio)

        output = "output/ai_sales_video.mp4"

        print("=" * 60)
        print("Rendering Final Video...")
        print("=" * 60)

        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=24,

            preset="ultrafast",

            bitrate="2000k",

            threads=1,

            logger=None

        )

        if audio:

            audio.close()

        for clip in clips:

            clip.close()

        final.close()

        del clips
        del final

        gc.collect()

        print("=" * 60)
        print("Rendering completed.")
        print(output)
        print("=" * 60)

        return output
