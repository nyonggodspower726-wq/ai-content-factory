from brain.story_splitter import split_story


class SceneEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB SCENE ENGINE")
        print("=" * 60)

    def generate(

        self,

        prompts,

        script

    ):

        print("Creating visual storyboard...")

        storyboard = split_story(script)

        scenes = []

        for item in storyboard:

            description = item.get(

                "description",

                ""

            ).strip()

            if not description:

                continue

            scene = {

                "scene_id": item.get(

                    "scene",

                    len(scenes) + 1

                ),

                "prompt": description,

                "duration": 5,

                "camera": "cinematic",

                "transition": "fade",

                "effect": "ken_burns"

            }

            scenes.append(scene)

        print("=" * 60)
        print(f"{len(scenes)} cinematic scenes created.")
        print("=" * 60)

        return scenes
