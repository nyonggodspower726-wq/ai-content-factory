import random


class MotionEngine:

    def __init__(self):

        print("=" * 60)
        print("MOTION ENGINE")
        print("=" * 60)

        self.movements = [

            "slow_zoom",

            "zoom_out",

            "pan_left",

            "pan_right",

            "push_in",

            "pull_back",

            "static"

        ]

    def apply(self, timeline):

        if not timeline:

            return timeline

        print("=" * 60)
        print("Applying Motion Engine...")
        print("=" * 60)

        for scene in timeline:

            camera = scene.get("camera", "auto")

            # ---------------------------------
            # Automatic camera movement
            # ---------------------------------

            if camera == "auto":

                motion = random.choice(

                    self.movements

                )

            # ---------------------------------
            # Manual camera movement
            # ---------------------------------

            else:

                motion = camera

            scene["motion"] = motion

            print(

                f"Scene {scene.get('scene_id', scene.get('id'))}"

            )

            print(

                f"Camera : {camera}"

            )

            print(

                f"Motion : {motion}"

            )

            print("-" * 40)

        print("Motion Engine completed.")

        return timeline
