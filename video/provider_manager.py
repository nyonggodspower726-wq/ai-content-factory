from video.wan_worker import generate_wan_video

# Future providers
# from video.cosmos_worker import generate_cosmos_video
# from video.fal_worker import generate_fal_video
# from video.replicate_worker import generate_replicate_video
# from video.comfy_worker import generate_comfy_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            {
                "name": "WAN 2.2",
                "function": generate_wan_video
            },

            # Uncomment when each provider is ready

            # {
            #     "name": "NVIDIA Cosmos",
            #     "function": generate_cosmos_video
            # },

            # {
            #     "name": "Fal.ai",
            #     "function": generate_fal_video
            # },

            # {
            #     "name": "Replicate",
            #     "function": generate_replicate_video
            # },

            # {
            #     "name": "ComfyUI",
            #     "function": generate_comfy_video
            # }

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
