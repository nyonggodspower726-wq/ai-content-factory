from video.wan import generate as wan_generate
from video.cogvideo import generate as cog_generate
from video.ltx import generate as ltx_generate
from video.minimax import generate as minimax_generate
from video.pexels import generate as pexels_generate
from video.unsplash import generate as unsplash_generate


class AIVideoRouter:

    def generate(self, prompt):

        providers = [

            ("WAN", wan_generate),

            ("CogVideo", cog_generate),

            ("LTX", ltx_generate),

            ("MiniMax", minimax_generate),

            ("Pexels", pexels_generate),

            ("Unsplash", unsplash_generate)

        ]

        for name, engine in providers:

            try:

                print(f"Trying {name}...")

                result = engine(prompt)

                if result:

                    print(f"{name} Success")

                    return result

            except Exception as e:

                print(f"{name} Failed")

                print(e)

        return None


router = AIVideoRouter()
