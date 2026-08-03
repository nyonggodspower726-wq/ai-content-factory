from video.wan_worker import generate_wan_video

# Future video providers can be added here
# from video.nvidia_worker import generate_nvidia_video


class VideoProviderManager:


    def __init__(self):

        self.providers = [

            generate_wan_video,

            # generate_nvidia_video,

        ]



    def generate(self, prompt):


        for provider in self.providers:


            try:

                print("=" * 50)
                print(
                    f"TRYING VIDEO PROVIDER: {provider.__name__}"
                )
                print("=" * 50)



                result = provider(
                    prompt
                )



                if result:


                    print("=" * 50)
                    print(
                        f"{provider.__name__} SUCCESS"
                    )
                    print("=" * 50)


                    return result



            except Exception as e:


                print("=" * 50)

                print(
                    f"{provider.__name__} FAILED"
                )

                print(
                    str(e)
                )

                print("=" * 50)



        print("=" * 50)
        print(
            "ALL VIDEO PROVIDERS FAILED"
        )
        print("=" * 50)



        return None




provider_manager = VideoProviderManager()
