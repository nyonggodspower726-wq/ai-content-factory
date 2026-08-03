from video.minimax_worker import generate_minimax_video
from video.wan_worker import generate_wan_video


# Future providers
# from video.cosmos_worker import generate_cosmos_video
# from video.replicate_worker import generate_replicate_video
# from video.comfy_worker import generate_comfy_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            {
                "name": "MiniMax H3 (Fal AI)",
                "function": generate_minimax_video
            },


            {
                "name": "WAN 2.2 (Hugging Face)",
                "function": generate_wan_video
            },


            # Future expansion

            # {
            #     "name": "NVIDIA Cosmos",
            #     "function": generate_cosmos_video
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
        print("PROMPTPROHUB VIDEO PROVIDER MANAGER")
        print("=" * 60)


        for provider in self.providers:

            print(
                f"Trying {provider['name']}..."
            )


            try:

                result = provider["function"](prompt)


                if result:

                    print(
                        f"{provider['name']} SUCCESS"
                    )

                    return result


                else:

                    print(
                        f"{provider['name']} failed - no output"
                    )


            except Exception as e:

                print(
                    f"{provider['name']} ERROR"
                )

                print(e)



        print("=" * 60)
        print("ALL VIDEO PROVIDERS FAILED")
        print("=" * 60)


        return None



provider_manager = VideoProviderManager()
