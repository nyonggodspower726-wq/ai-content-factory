from video.open_source_manager import open_source_manager
import time


def generate_scene(prompt):

    print("=" * 60)
    print("GENERATING AI SCENE")
    print("=" * 60)

    attempts = 0

    while attempts < 3:

        attempts += 1

        print(f"Attempt {attempts}")

        try:

            scene = open_source_manager.generate(prompt)

            if scene:

                print("Scene generated successfully.")

                return scene

        except Exception as e:

            print(e)

        print("Retrying in 5 seconds...")

        time.sleep(5)

    print("Scene generation failed.")

    return None



def generate_all_scenes(prompts):

    scenes = []

    prompts = prompts[:6]

    print("=" * 60)
    print("AI VIDEO FACTORY")
    print("=" * 60)

    for index, prompt in enumerate(prompts):

        print(f"Generating Scene {index + 1}")

        scene = generate_scene(prompt)

        if scene:

            scenes.append(scene)

        else:

            print(f"Scene {index + 1} skipped.")

    print("=" * 60)
    print(f"TOTAL SCENES GENERATED: {len(scenes)}")
    print("=" * 60)

    return scenes
