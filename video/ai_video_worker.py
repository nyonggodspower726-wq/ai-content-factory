from video.provider_manager import provider_manager


def generate_scene(prompt):

    print("=" * 50)
    print("Generating AI Scene")
    print("=" * 50)

    return provider_manager.generate(prompt)


def generate_all_scenes(prompts):

    scenes = []

    for index, prompt in enumerate(prompts):

        print(f"Scene {index + 1}")

        scene = generate_scene(prompt)

        if scene:

            scenes.append(scene)

        else:

            print(
                f"Scene {index + 1} failed."
            )

    return scenes
