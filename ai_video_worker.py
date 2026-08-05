from video.ai_video_router import router
import time


# ============================================================
# GENERATE ONE SCENE
# ============================================================

def generate_scene(prompt):

    print("=" * 60)
    print("PROMPTPROHUB AI SCENE GENERATOR")
    print("=" * 60)

    max_attempts = 5

    for attempt in range(1, max_attempts + 1):

        print(f"Attempt {attempt}/{max_attempts}")

        try:

            scene = router.generate(prompt)

            if scene:

                print("Scene generated successfully.")

                return scene

            print("Provider returned no result.")

        except Exception as e:

            print(f"Generation Error: {e}")

        if attempt < max_attempts:

            print("Retrying in 8 seconds...")
            time.sleep(8)

    print("Scene generation completely failed.")

    return None


# ============================================================
# GENERATE ALL SCENES
# ============================================================

def generate_all_scenes(prompts):

    scenes = []

    if not prompts:

        print("=" * 60)
        print("No prompts received.")
        print("=" * 60)
        return scenes

    # Maximum scenes supported
    prompts = prompts[:8]

    print("=" * 60)
    print("PROMPTPROHUB AI VIDEO FACTORY")
    print("=" * 60)

    total = len(prompts)

    for index, prompt in enumerate(prompts, start=1):

        print("=" * 60)
        print(f"Generating Scene {index}/{total}")
        print("=" * 60)

        scene = generate_scene(prompt)

        if scene:

            scenes.append(scene)

            print(f"Scene {index} Complete")

        else:

            print(f"Scene {index} Failed - continuing...")

    print("=" * 60)
    print("VIDEO FACTORY REPORT")
    print("=" * 60)
    print(f"Requested Scenes : {total}")
    print(f"Generated Scenes : {len(scenes)}")
    print(f"Failed Scenes    : {total - len(scenes)}")
    print("=" * 60)

    return scenes
