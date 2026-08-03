from video.provider_manager import provider_manager
import time



def generate_scene(prompt, scene_number):

    print("=" * 60)
    print(f"GENERATING SCENE {scene_number}")
    print("=" * 60)


    attempts = 0


    while attempts < 3:

        attempts += 1


        print(
            f"Attempt {attempts}/3"
        )


        try:

            scene = provider_manager.generate(
                prompt
            )


            if scene:

                print(
                    f"Scene {scene_number} completed"
                )

                return {
                    "scene": scene_number,
                    "video": scene,
                    "status": "SUCCESS"
                }


            else:

                print(
                    "Provider returned no video"
                )


        except Exception as e:

            print(
                "Scene generation error:"
            )

            print(e)



        if attempts < 3:

            print(
                "Retrying in 10 seconds..."
            )

            time.sleep(10)



    print(
        f"Scene {scene_number} failed"
    )


    return {
        "scene": scene_number,
        "video": None,
        "status": "FAILED"
    }




def generate_all_scenes(prompts):


    if not prompts:

        print(
            "No scene prompts received"
        )

        return []



    videos = []


    # Production limit
    prompts = prompts[:6]



    for index, prompt in enumerate(prompts, start=1):


        result = generate_scene(
            prompt,
            index
        )


        if result["video"]:

            videos.append(
                result["video"]
            )


        else:

            print(
                f"Skipping failed scene {index}"
            )



    print("=" * 60)

    print(
        f"TOTAL SUCCESSFUL SCENES: {len(videos)}"
    )

    print("=" * 60)



    return videos
