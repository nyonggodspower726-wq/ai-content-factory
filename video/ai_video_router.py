import time
import os


# ============================================================
# VIDEO PROVIDERS
# ============================================================

try:
    from video.minimax_worker import generate_minimax_video
except Exception:
    generate_minimax_video = None


try:
    from video.wan_worker import generate_wan_video
except Exception:
    generate_wan_video = None


try:
    from video.pexels_worker import generate_pexels_video
except Exception:
    generate_pexels_video = None


try:
    from video.unsplash_worker import generate_unsplash_video
except Exception:
    generate_unsplash_video = None



# ============================================================
# ROUTER SETTINGS
# ============================================================

PRIMARY_PROVIDER = "MiniMax"



# ============================================================
# AI VIDEO ROUTER
# ============================================================

class AIVideoRouter:


    def generate(self, prompt):


        providers = {

            "MiniMax": generate_minimax_video,

            "WAN": generate_wan_video,

            "Pexels": generate_pexels_video,

            "Unsplash": generate_unsplash_video

        }



        order = list(providers.keys())


        # Put primary provider first

        if PRIMARY_PROVIDER in order:

            order.remove(
                PRIMARY_PROVIDER
            )

            order.insert(
                0,
                PRIMARY_PROVIDER
            )



        for name in order:


            engine = providers[name]


            if engine is None:

                print(
                    f"{name} unavailable - skipping"
                )

                continue



            print("=" * 60)
            print(
                f"TRYING VIDEO PROVIDER: {name}"
            )
            print("=" * 60)



            try:


                start = time.time()


                result = engine(
                    prompt
                )


                elapsed = round(
                    time.time() - start,
                    2
                )



                if result:


                    print(
                        f"{name} SUCCESS"
                    )

                    print(
                        f"Generation time: {elapsed}s"
                    )


                    return result



                print(
                    f"{name} returned empty result"
                )



            except Exception as e:


                print(
                    f"{name} FAILED"
                )

                print(
                    e
                )



            print(
                "Moving to next provider..."
            )


            time.sleep(3)



        print("=" * 60)
        print(
            "NO VIDEO PROVIDER AVAILABLE"
        )
        print("=" * 60)


        return None





router = AIVideoRouter()
