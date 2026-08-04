import time


# ============================================================
# VIDEO PROVIDERS
# ============================================================

try:
    from video.coverr_worker import generate_coverr_video
except Exception:
    generate_coverr_video = None

try:
    from video.pexels_worker import generate_pexels_video
except Exception:
    generate_pexels_video = None

try:
    from video.unsplash_worker import generate_unsplash_video
except Exception:
    generate_unsplash_video = None

try:
    from video.minimax_worker import generate_minimax_video
except Exception:
    generate_minimax_video = None

try:
    from video.wan_worker import generate_wan_video
except Exception:
    generate_wan_video = None


# ============================================================
# AI VIDEO ROUTER
# ============================================================

class AIVideoRouter:

    def generate(self, prompt):

        providers = {

            "Coverr": generate_coverr_video,

            "Pexels": generate_pexels_video,

            "Unsplash": generate_unsplash_video,

            "MiniMax": generate_minimax_video,

            "WAN": generate_wan_video,

        }

        # Fixed provider order
        order = [
            "Coverr",
            "Pexels",
            "Unsplash",
            "MiniMax",
            "WAN"
        ]

        for name in order:

            engine = providers.get(name)

            if engine is None:

                print(f"{name} unavailable - skipping")

                continue

            print("=" * 60)
            print(f"TRYING VIDEO PROVIDER: {name}")
            print("=" * 60)

            try:

                start = time.time()

                result = engine(prompt)

                elapsed = round(time.time() - start, 2)

                if result:

                    print(f"{name} SUCCESS")
                    print(f"Generation time: {elapsed}s")

                    return result

                print(f"{name} returned empty result")

            except Exception as e:

                print(f"{name} FAILED")
                print(e)

            print("Switching provider...")

            time.sleep(3)

        print("=" * 60)
        print("ALL VIDEO PROVIDERS FAILED")
        print("=" * 60)

        return None


router = AIVideoRouter()
