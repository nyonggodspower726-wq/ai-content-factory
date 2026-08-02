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

        available = []

        for provider in self.providers:

            if api_manager.get(provider):

                available.append(provider)

        return available


failover = FailoverEngine()
