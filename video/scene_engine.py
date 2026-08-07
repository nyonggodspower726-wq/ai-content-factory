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

        scenes = []

        if not prompts:

            prompts = script.split(".")


        if isinstance(prompts, dict):

            prompts = prompts.get(
                "scenes",
                []
            )


        if isinstance(prompts, str):

            prompts = [prompts]


        for index, prompt in enumerate(prompts):

            if isinstance(prompt, dict):

                prompt = prompt.get(
                    "prompt",
                    ""
                )

            prompt = str(prompt).strip()

            if not prompt:
                continue

            search_prompt = self.optimize_prompt(prompt)

            scene = {

                "scene_id": index + 1,

                "prompt": search_prompt,

                "duration": 5,

                "camera": "cinematic",

                "transition": "fade",

                "effect": "documentary"

            }

            scenes.append(scene)

        print(f"{len(scenes)} scenes generated.")

        return scenes


    def optimize_prompt(self, prompt):

        prompt = prompt.lower()

        if "chatgpt" in prompt or "ai prompt" in prompt:

            return "young entrepreneur using laptop in modern office"

        if "business" in prompt:

            return "business owner working in modern office"

        if "marketing" in prompt:

            return "digital marketer working on laptop"

        if "freelancer" in prompt:

            return "freelancer working from home office"

        if "content" in prompt:

            return "content creator at computer desk"

        if "automation" in prompt:

            return "professional using AI software on laptop"

        if "money" in prompt:

            return "successful entrepreneur office workspace"

        if "website" in prompt:

            return "web designer working on laptop"

        return "professional working on laptop in modern office"
