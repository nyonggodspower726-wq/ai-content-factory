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

        print("=" * 60)
        print("Applying Transition Engine...")
        print("=" * 60)

        total = len(timeline)

        for index, scene in enumerate(timeline):

            transition = scene.get(
                "transition",
                "auto"
            )

            # -----------------------------
            # Last scene
            # -----------------------------

            if index == total - 1:

                transition = "none"

            # -----------------------------
            # Automatic transition
            # -----------------------------

            elif transition == "auto":

                transition = random.choice(

                    self.transitions[:-1]

                )

            # -----------------------------
            # Save transition
            # -----------------------------

            scene["transition"] = transition

            print(

                f"Scene {scene.get('scene_id', scene.get('id'))}"

            )

            print(

                f"Transition : {transition}"

            )

            print("-" * 40)

        print("Transition Engine completed.")

        return timeline
