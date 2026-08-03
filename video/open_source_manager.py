from video.wan_worker import generate_wan_video
from video.ltx_worker import generate_ltx_video
from video.cogvideo_worker import generate_cogvideo_video


class OpenSourceVideoManager:

    def __init__(self):

        self.providers = [

            {
                "name": "WAN 2.2",
                "function": generate_wan_video
            },

            {
                "name": "LTX Video",
                "function": generate_ltx_video
            },

            {
                "name": "CogVideoX",
                "function": generate_cogvideo_video
            }

        ]

    def generate(self, prompt):

        print("=" * 60)
        print("PROMPTPROHUB OPEN SOURCE VIDEO ENGINE")
        print("=" * 60)

        for provider in self.providers:

            print(f"Trying {provider['name']}...")

            try:

                result = provider["function"](prompt)

                if result:

                    print(f"{provider['name']} generated video.")

                    return result

                else:

                    print(f"{provider['name']} unavailable.")

            except Exception as e:

                print(f"{provider['name']} failed.")

                print(str(e))

        print("=" * 60)
        print("NO OPEN SOURCE VIDEO MODEL AVAILABLE")
        print("=" * 60)

        return None

    def available_models(self):

        return [

            provider["name"]

            for provider in self.providers

        ]


open_source_manager = OpenSourceVideoManager()
