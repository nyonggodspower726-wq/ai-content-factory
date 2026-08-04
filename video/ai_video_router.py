from video.wan_worker import generate_wan_video
from video.cogvideo_worker import generate_cogvideo_video
from video.ltx_worker import generate_ltx_video
from video.minimax_worker import generate_minimax_video
from video.pexels_worker import generate_pexels_video
from video.unsplash_worker import generate_unsplash_video


class AIVideoRouter:

    def generate(self, prompt):

        providers = [

            ("WAN 2.2", generate_wan_video),

            ("CogVideoX", generate_cogvideo_video),

            ("LTX", generate_ltx_video),

            ("MiniMax", generate_minimax_video),

            ("Pexels", generate_pexels_video),

            ("Unsplash", generate_unsplash_video)

        ]

        for name, engine in providers:

            try:

                print("=" * 60)
                print(f"TRYING {name}")
                print("=" * 60)

                result = engine(prompt)

                if result:

                    print(f"{name} Success")

                    return result

                else:

                    print(f"{name} unavailable")

            except Exception as e:

                print(f"{name} Failed")
                print(e)

        print("=" * 60)
        print("NO AI VIDEO PROVIDER AVAILABLE")
        print("=" * 60)

        return None


router = AIVideoRouter()
