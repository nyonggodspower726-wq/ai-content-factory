from video.ai_video_router import router
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

            scene = router.generate(prompt)

            if scene is not None:

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

    if prompts is None:

        print("No prompts received.")

        return scenes

    prompts = prompts[:6]

    print("=" * 60)
    print("PROMPTPROHUB AI VIDEO FACTORY")
    print("=" * 60)

    for index, prompt in enumerate(prompts):

        print("=" * 60)
        print(f"Generating Scene {index + 1}")
        print("=" * 60)

        scene = generate_scene(prompt)

        if scene:

            scenes.append(scene)

            print(f"Scene {index + 1} Complete")

        else:

            print(f"Scene {index + 1} Failed")

    print("=" * 60)
    print(f"TOTAL SCENES GENERATED: {len(scenes)}")
    print("=" * 60)

    return scenes
