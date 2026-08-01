from video.wan_worker import generate_wan_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            generate_wan_video,

        ]


    def generate(self, prompt):

        for provider in self.providers:

            try:

                print(
                    f"Trying {provider.__name__}"
                )

                result = provider(prompt)

                if result:

                    print(
                        "Video generated successfully."
                    )

                    return result

            except Exception as e:

                print(e)

        print(
            "All providers failed."
        )

        return None


provider_manager = VideoProviderManager()
