import random


class TransitionEngine:

    def __init__(self):

        print("=" * 60)
        print("TRANSITION ENGINE")
        print("=" * 60)

        self.transitions = [

            "fade",

            "crossfade",

            "slide_left",

            "slide_right",

            "zoom",

            "blur",

            "flash",

            "none"

        ]

    def apply(self, timeline):

        if not timeline:

            return timeline

        print("Applying transitions...")

        total = len(timeline)

        for index, scene in enumerate(timeline):

            # Last scene doesn't need a transition
            if index == total - 1:

                scene["transition"] = "none"

            elif scene.get("transition") == "auto":

                scene["transition"] = random.choice(
                    self.transitions[:-1]
                )

            elif "transition" not in scene:

                scene["transition"] = "fade"

            print(
                f"Scene {scene.get('scene_id', scene.get('id'))}: "
                f"{scene['transition']}"
            )

        return timeline
