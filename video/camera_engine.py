import random

from moviepy.editor import vfx


CAMERA_MOVES = [

    "slow_zoom",

    "zoom_out",

    "pan_left",

    "pan_right",

    "push_in",

    "pull_back",

    "static"

]


def apply_camera_effects(timeline):

    if not timeline:

        return timeline

    print("=" * 60)
    print("CAMERA ENGINE")
    print("=" * 60)

    for scene in timeline:

        clip = scene.get("clip_object")

        if clip is None:

            continue

        motion = scene.get("motion")

        if motion is None:

            motion = random.choice(
                CAMERA_MOVES
            )

            scene["motion"] = motion

        try:

            # ---------------------------------
            # Slow Zoom
            # ---------------------------------

            if motion == "slow_zoom":

                clip = clip.fx(

                    vfx.resize,

                    lambda t: 1 + (
                        0.05 * t / clip.duration
                    )

                )

            # ---------------------------------
            # Zoom Out
            # ---------------------------------

            elif motion == "zoom_out":

                clip = clip.fx(

                    vfx.resize,

                    lambda t: 1.05 - (
                        0.05 * t / clip.duration
                    )

                )

            # ---------------------------------
            # Push In
            # ---------------------------------

            elif motion == "push_in":

                clip = clip.fx(

                    vfx.resize,

                    1.08

                )

            # ---------------------------------
            # Pull Back
            # ---------------------------------

            elif motion == "pull_back":

                clip = clip.fx(

                    vfx.resize,

                    0.95

                )

            # ---------------------------------
            # Pan Left
            # (placeholder)
            # ---------------------------------

            elif motion == "pan_left":

                print("Pan Left ready.")

            # ---------------------------------
            # Pan Right
            # (placeholder)
            # ---------------------------------

            elif motion == "pan_right":

                print("Pan Right ready.")

            # ---------------------------------
            # Static
            # ---------------------------------

            else:

                print("Static camera.")

            scene["clip_object"] = clip

            print(

                f"Scene {scene.get('scene_id')} -> {motion}"

            )

        except Exception as e:

            print(

                f"Camera Engine Error: {e}"

            )

    return timeline
