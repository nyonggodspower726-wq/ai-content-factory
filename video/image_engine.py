from video.image_provider import generate_ai_image


class ImageEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB IMAGE ENGINE")
        print("=" * 60)

    def generate(self, scenes):

        if not scenes:

            return []

        print("Generating AI images...")

        results = []

        for scene in scenes:

            prompt = scene.get("prompt", "")

            # Make every prompt cinematic
            cinematic_prompt = (
                f"{prompt}, "
                "ultra realistic, cinematic lighting, "
                "8k, highly detailed, masterpiece, "
                "professional photography, "
                "depth of field, volumetric lighting, "
                "vertical composition 9:16"
            )

            image = generate_ai_image(

                cinematic_prompt

            )

            scene["image"] = image

            results.append(scene)

            print(
                f"Scene {scene.get('scene_id')} image ready."
            )

        print(
            f"{len(results)} AI images generated."
        )

        return results
