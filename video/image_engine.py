from video.pexels_provider import generate_ai_image


class ImageEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB PEXELS IMAGE ENGINE")
        print("=" * 60)

    def generate(self, scenes):

        if not scenes:
            return []

        print("Generating realistic business images...")

        results = []

        for scene in scenes:

            prompt = scene.get(
                "prompt",
                ""
            )

            image = generate_ai_image(
                prompt
            )

            scene["image"] = image

            results.append(
                scene
            )

            print(
                f"Scene {scene.get('scene', 'unknown')} image ready."
            )

        print(
            f"{len(results)} images generated."
        )

        return results
