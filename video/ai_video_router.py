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


            print("=" * 60)
            print(f"TRYING {name}")
            print("=" * 60)


            try:

                result = engine(prompt)


                if result:

                    print(
                        f"{name} SUCCESS"
                    )

                    return result


                print(
                    f"{name} returned nothing"
                )


            except Exception as e:

                print(
                    f"{name} FAILED"
                )

                print(str(e))



        print("=" * 60)
        print("ALL VIDEO PROVIDERS FAILED")
        print("=" * 60)

        return None



router = AIVideoRouter()
