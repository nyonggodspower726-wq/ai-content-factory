import json
import os
from datetime import datetime


class CreditManager:

    def __init__(self):

        self.file = "brain/credits.json"

        os.makedirs("brain", exist_ok=True)

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump({

                    "groq": 0,

                    "video": 0,

                    "voice": 0,

                    "today": datetime.now().strftime("%Y-%m-%d")

                }, f, indent=4)

    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)

    def save(self, data):

        with open(self.file, "w") as f:

            json.dump(data, f, indent=4)

    def use_groq(self):

        data = self.load()

        data["groq"] += 1

        self.save(data)

    def use_video(self):

        data = self.load()

        data["video"] += 1

        self.save(data)

    def use_voice(self):

        data = self.load()

        data["voice"] += 1

        self.save(data)

    def report(self):

        return self.load()


credits = CreditManager()
