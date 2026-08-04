from video.minimax_worker import generate_minimax_video
from video.wan_worker import generate_wan_video
from video.pexels_worker import generate_pexels_video
from video.unsplash_worker import generate_unsplash_video


class AIVideoRouter:

    def generate(self, prompt):

        providers = [

            ("MiniMax H3", generate_minimax_video),

            ("WAN 2.2", generate_wan_video),

            ("Pexels", generate_pexels_video),

            ("Unsplash", generate_unsplash_video)

        ]


        for name, engine in providers:

            try:

                print("=" * 50)
                print(f"TRYING {name}")
                print("=" * 50)


                result = engine(prompt)


                if result:

                    print(
                        f"{name} SUCCESS"
                    )

                    return result


                print(
                    f"{name} unavailable"
                )


            except Exception as e:

                print(
                    f"{name} failed"
                )

                print(e)


        print(
            "ALL VIDEO ENGINES FAILED"
        )

        return None


router = AIVideoRouter()
