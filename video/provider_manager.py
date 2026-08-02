from video.wan_worker import generate_wan_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            generate_wan_video,

        ]


    def generate(self, prompt):

        for provider in self.providers:

            try:

                print("=" * 50)
                print(f"Trying {provider.__name__}")
                print("=" * 50)


                result = provider(prompt)


                if result:

                    print(
                        "Video generated successfully."
                    )

                    return result


            except Exception as e:

                print(
                    f"{provider.__name__} failed:"
                )

                print(
                    str(e)
                )


        print("=" * 50)
        print("All video providers failed.")
        print("=" * 50)


        return None



provider_manager = VideoProviderManager()
