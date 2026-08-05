from video.wan_worker import generate_wan_video
from video.cogvideo_worker import generate_cogvideo_video
from video.ltx_worker import generate_ltx_video

from video.minimax_worker import generate_minimax_video
from video.pexels_worker import generate_pexels_video
from video.unsplash_worker import generate_unsplash_video


class OpenSourceVideoManager:

    def __init__(self):

        self.providers = [

            {
                "name": "WAN 2.2",
                "function": generate_wan_video
            },

            {
                "name": "CogVideoX",
                "function": generate_cogvideo_video
            },

            {
                "name": "LTX Video",
                "function": generate_ltx_video
            },

            {
                "name": "MiniMax",
                "function": generate_minimax_video
            },

            {
                "name": "Pexels",
                "function": generate_pexels_video
            },

            {
                "name": "Unsplash",
                "function": generate_unsplash_video
            }

        ]

    def generate(self, prompt):

        print("=" * 60)
        print("PROMPTPROHUB AI VIDEO ROUTER")
        print("=" * 60)

        for provider in self.providers:

            print(f"Trying {provider['name']}...")

            try:

                result = provider["function"](prompt)

                if result is not None:

                    print(f"{provider['name']} Success")

                    return result

                print(f"{provider['name']} returned no video")

            except Exception as e:

                print(f"{provider['name']} Failed")

                print(e)

        print("=" * 60)
        print("ALL VIDEO PROVIDERS FAILED")
        print("=" * 60)

        return None

    def available_models(self):

        return [

            provider["name"]

            for provider in self.providers

        ]


open_source_manager = OpenSourceVideoManager()
