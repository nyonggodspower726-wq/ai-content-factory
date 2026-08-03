import json
import os


class ProviderMemory:

    def __init__(self):

        self.file = "brain/memory/provider_memory.json"

        os.makedirs("brain/memory", exist_ok=True)

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump({}, f, indent=4)


    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)


    def save(self, data):

        with open(self.file, "w") as f:

            json.dump(data, f, indent=4)


    def remember(self, provider):

        data = self.load()

        if provider not in data:

            data[provider] = {

                "uses": 0,

                "success": 0,

                "failed": 0

            }

        data[provider]["uses"] += 1

        self.save(data)


    def success(self, provider):

        data = self.load()

        if provider in data:

            data[provider]["success"] += 1

            self.save(data)


    def failed(self, provider):

        data = self.load()

        if provider in data:

            data[provider]["failed"] += 1

            self.save(data)


    def report(self):

        return self.load()


    def best_provider(self):

        data = self.load()

        if not data:

            return None

        best = max(

            data.items(),

            key=lambda x: x[1]["success"]

        )

        return best[0]


    def clear(self):

        self.save({})


provider_memory = ProviderMemory()
