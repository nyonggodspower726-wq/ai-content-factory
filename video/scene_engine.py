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


        # ---------------------------------
        # Use script if no prompts received
        # ---------------------------------

        if not prompts:

            prompts = script.split(".")



        # ---------------------------------
        # Handle dictionary input
        # ---------------------------------

        if isinstance(prompts, dict):

            prompts = prompts.get(

                "scenes",

                []

            )



        # ---------------------------------
        # Convert single prompt to list
        # ---------------------------------

        if isinstance(prompts, str):

            prompts = [

                prompts

            ]



        # ---------------------------------
        # Build scenes
        # ---------------------------------

        for index, prompt in enumerate(prompts):


            if isinstance(prompt, dict):

                prompt = prompt.get(

                    "prompt",

                    ""

                )


            prompt = str(prompt).strip()


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



        print(

            f"{len(scenes)} scenes generated."

        )


        return scenes
