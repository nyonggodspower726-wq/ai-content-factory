from video.wan_worker import generate_wan_video


# Optional providers
try:
    from video.minimax_worker import generate_minimax_video
except Exception:
    generate_minimax_video = None


try:
    from video.pexels_worker import generate_pexels_video
except Exception:
    generate_pexels_video = None


try:
    from video.unsplash_worker import generate_unsplash_video
except Exception:
    generate_unsplash_video = None



class AIVideoRouter:


    def generate(self, prompt):


        providers = [

            (
                "WAN 2.2",
                generate_wan_video
            ),


            (
                "MiniMax H3",
                generate_minimax_video
            ),


            (
                "Pexels",
                generate_pexels_video
            ),


            (
                "Unsplash",
                generate_unsplash_video
            )

        ]



        for name, engine in providers:


            if engine is None:

                print(
                    f"{name} not available - skipping"
                )

                continue



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


                print(
                    str(e)
                )




        print("=" * 60)
        print("ALL VIDEO PROVIDERS FAILED")
        print("=" * 60)



        return None




router = AIVideoRouter()
