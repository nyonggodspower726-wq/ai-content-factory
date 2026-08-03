from video.minimax_worker import generate_minimax_video
from video.fal_worker import generate_fal_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            {
                "name": "MiniMax H3",
                "function": generate_minimax_video
            },

            {
                "name": "Fal AI",
                "function": generate_fal_video
            }

        ]

    def generate(self, prompt):

        print("=" * 60)
        print("VIDEO PROVIDER MANAGER")
        print("=" * 60)

        for provider in self.providers:

            print(f"Trying {provider['name']}...")

            try:

                result = provider["function"](prompt)

                if result:

                    print(f"{provider['name']} succeeded.")

                    return result

                else:

                    print(f"{provider['name']} returned nothing.")

            except Exception as e:

                print(f"{provider['name']} failed.")

                print(str(e))

        print("=" * 60)
        print("NO VIDEO PROVIDER SUCCEEDED")
        print("=" * 60)

        return None


provider_manager = VideoProviderManager()
