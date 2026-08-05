import os


class ClipEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB CLIP ENGINE")
        print("=" * 60)

    def generate(self, prompts):

        clips = []

        if prompts is None:
            print("No prompts received.")
            return clips

        if isinstance(prompts, str):
            prompts = [prompts]

        for index, prompt in enumerate(prompts):

            scene = {
                "id": index + 1,
                "prompt": prompt,
                "duration": 5,
                "style": "cinematic",
                "camera": "auto",
                "transition": "fade",
                "clip": None
            }

            print(f"Scene {index + 1}")
            print(f"Prompt: {prompt}")

            clips.append(scene)

        print(f"Created {len(clips)} scenes.")

        return clips
