from brain.api_manager import api_manager


class FailoverEngine:

    def __init__(self):

        self.providers = [

            "groq",

            "google",

            "nvidia",

            "huggingface"

        ]


    def available(self):

        return api_manager.available()


    def next_provider(self):

        providers = self.available()

        if not providers:

            return None

        return providers[0]


    def disable(self, provider):

        api_manager.disable(provider)


    def enable(self, provider):

        api_manager.enable(provider)


failover = FailoverEngine()
