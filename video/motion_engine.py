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

        print("Applying cinematic motion...")

        for scene in timeline:

            if scene.get("camera") == "auto":

                scene["motion"] = random.choice(
                    self.movements
                )

            else:

                scene["motion"] = scene["camera"]

            print(
                f"Scene {scene.get('scene_id', scene.get('id'))}: "
                f"{scene['motion']}"
            )

        return timeline
