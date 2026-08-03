from video.provider_manager import provider_manager
import time



def generate_scene(prompt):

    print("=" * 50)
    print("GENERATING AI SCENE")
    print("=" * 50)

    attempts = 0
    scene = None


    while attempts < 3 and not scene:

        attempts += 1

        print(
            f"Scene generation attempt {attempts}"
        )


        try:

            scene = provider_manager.generate(
                prompt
            )


            if scene:

                print(
                    "Scene generated successfully"
                )

                return scene


        except Exception as e:

            print(
                "Scene generation error:"
            )

            print(e)


        time.sleep(5)


    print(
        "Scene generation failed after retries"
    )

    return None




def generate_all_scenes(prompts):

    scenes = []


    # Safety limit
    prompts = prompts[:6]


    for index, prompt in enumerate(prompts):

        print("=" * 50)
        print(
            f"GENERATING SCENE {index + 1}"
        )
        print("=" * 50)


        scene = generate_scene(
            prompt
        )


        if scene:

            scenes.append(scene)


        else:

            print(
                f"Scene {index + 1} skipped"
            )


    print("=" * 50)
    print(
        f"TOTAL SCENES CREATED: {len(scenes)}"
    )
    print("=" * 50)


    return scenes
