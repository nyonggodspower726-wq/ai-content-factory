import os


class APIManager:

    def __init__(self):

        self.providers = {

            "groq": os.getenv("GROQ_API_KEY"),

            "google": os.getenv("GOOGLE_API_KEY"),

            "nvidia": os.getenv("NVIDIA_API_KEY"),

            "huggingface": os.getenv("HF_API_TOKEN"),

        }


    def get(self, provider):

        return self.providers.get(provider)


api_manager = APIManager()
