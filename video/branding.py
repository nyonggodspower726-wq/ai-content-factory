import os

from moviepy.editor import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
)


class BrandingEngine:

    def __init__(self):

        self.brand_name = "PromptProHub"

        self.website = "https://promptprohub.com"

        self.logo = "assets/logos/logo.png"

        print("=" * 60)
        print("BRANDING ENGINE READY")
        print("=" * 60)

    def apply(

        self,

        video_path,

        hook_text=None

    ):

        if not os.path.exists(video_path):

            print("Video not found.")

            return video_path

        video = VideoFileClip(video_path)

        clips = [video]

        # -------------------------------------
        # Hook Text
        # -------------------------------------

        if hook_text:

            hook = (

                TextClip(

                    hook_text,

                    fontsize=70,

                    color="white",

                    stroke_color="black",

                    stroke_width=3,

                    method="caption",

                    size=(900, None),

                    align="center"

                )

                .set_position(("center", 120))

                .set_duration(5)

            )

            clips.append(hook)

        # -------------------------------------
        # Watermark
        # -------------------------------------

        watermark = (

            TextClip(

                self.brand_name,

                fontsize=35,

                color="white",

                method="label"

            )

            .set_position(("right", "bottom"))

            .set_duration(video.duration)

        )

        clips.append(watermark)

        # -------------------------------------
        # Website
        # -------------------------------------

        website = (

            TextClip(

                self.website,

                fontsize=28,

                color="yellow",

                method="label"

            )

            .set_position(("center", "bottom"))

            .set_duration(video.duration)

        )

        clips.append(website)

        final = CompositeVideoClip(clips)

        output = "output/branded_video.mp4"

        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=30,

            logger=None

        )

        video.close()

        final.close()

        print("Branding applied.")

        return output
