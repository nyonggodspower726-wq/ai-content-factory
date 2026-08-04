from brain.api_manager import api_manager


class FailoverEngine:

    def __init__(self):

        self.providers = [

            "groq",
            "google",
            "nvidia",
            "openrouter"

        ]

    def available(self):

        available = api_manager.available()

        ordered = []

        for provider in self.providers:

            if provider in available:

                ordered.append(provider)

        return ordered

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
