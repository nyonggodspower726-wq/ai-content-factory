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

            "huggingface": {
                "key": os.getenv("HF_API_TOKEN"),
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

        available = []

        for name, info in self.providers.items():

            if info["enabled"] and info["key"]:

                available.append(name)

        return available


api_manager = APIManager()
