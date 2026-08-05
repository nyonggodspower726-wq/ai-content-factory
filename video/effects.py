from moviepy.editor import (
    VideoFileClip,
    CompositeVideoClip,
    TextClip,
    vfx
)


class EffectsEngine:

    def __init__(self):

        print("=" * 60)
        print("VISUAL EFFECTS ENGINE")
        print("=" * 60)

    def apply(self, timeline):

        if not timeline:

            return timeline

        print("Applying cinematic effects...")

        for scene in timeline:

            clip = scene.get("clip_object")

            if clip is None:
                continue

            try:

                # Slight cinematic zoom
                clip = clip.fx(
                    vfx.resize,
                    1.02
                )

                # Fade in
                clip = clip.fadein(
                    0.5
                )

                # Fade out
                clip = clip.fadeout(
                    0.5
                )

                scene["clip_object"] = clip

                print(
                    f"Effects applied to Scene {scene.get('scene_id')}"
                )

            except Exception as e:

                print(e)

        return timeline


def add_hook(

    video_path,

    hook_text

):

    try:

        video = VideoFileClip(video_path)

        hook = (

            TextClip(

                hook_text,

                fontsize=65,

                color="white",

                stroke_color="black",

                stroke_width=3,

                method="caption",

                size=(900, None),

                align="center"

            )

            .set_duration(4)

            .set_position(("center", 100))

        )

        final = CompositeVideoClip(

            [

                video,

                hook

            ]

        )

        output = "output/hooked_video.mp4"

        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=30,

            logger=None

        )

        video.close()

        final.close()

        return output

    except Exception as e:

        print(e)

        return video_path
