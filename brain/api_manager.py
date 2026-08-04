import os


class APIManager:

    def __init__(self):

        self.providers = {

            "groq": {
                "key": os.getenv("GROQ_API_KEY"),
                "enabled": True
            },

            "google": {
                "key": os.getenv("GOOGLE_API_KEY"),
                "enabled": True
            },

            "nvidia": {
                "key": os.getenv("NVIDIA_API_KEY"),
                "enabled": True
            },

            "openrouter": {
                "key": os.getenv("OPENROUTER_API_KEY"),
                "enabled": True
            }

        }

    def get_key(self, provider):

        if provider not in self.providers:
            return None

        return self.providers[provider]["key"]

    def enabled(self, provider):

        if provider not in self.providers:
            return False

        return self.providers[provider]["enabled"]

    def disable(self, provider):

        if provider in self.providers:
            self.providers[provider]["enabled"] = False

    def enable(self, provider):

        if provider in self.providers:
            self.providers[provider]["enabled"] = True

    def available(self):

        print("=" * 60)
        print("API STATUS")
        print("=" * 60)

        available = []

        for name, info in self.providers.items():

            print(
                f"{name:<12}"
                f"Enabled: {info['enabled']} | "
                f"Key Exists: {bool(info['key'])}"
            )

            if info["enabled"] and info["key"]:

                available.append(name)

        print("-" * 60)
        print("AVAILABLE PROVIDERS:", available)
        print("=" * 60)

        return available


api_manager = APIManager()
