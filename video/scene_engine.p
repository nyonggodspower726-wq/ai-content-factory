class SceneEngine:

    def __init__(self):

        print("=" * 60)
        print("SCENE ENGINE")
        print("=" * 60)

    def generate(
        self,
        prompts,
        script
    ):

        scenes = []

        # If prompts is empty, use the script
        if not prompts:

            prompts = script.split(".")

        # Convert single prompt to list
        if isinstance(prompts, str):

            prompts = [prompts]

        for index, prompt in enumerate(prompts):

            prompt = prompt.strip()

            if not prompt:
                continue

            scene = {

                "scene_id": index + 1,

                "prompt": prompt,

                "duration": 5,

                "camera": "auto",

                "transition": "fade",

                "effect": "cinematic"

            }

            scenes.append(scene)

        print(f"{len(scenes)} scenes generated.")

        return scenes
