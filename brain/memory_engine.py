import os
import json
from datetime import datetime


MEMORY_FOLDER = "brain/memory"

os.makedirs(MEMORY_FOLDER, exist_ok=True)


class MemoryEngine:

    def __init__(self):

        self.file = os.path.join(
            MEMORY_FOLDER,
            "memory.json"
        )

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump([], f)


    def save(self, topic, result):

        with open(self.file, "r") as f:

            data = json.load(f)

        data.append({

            "time": datetime.now().isoformat(),

            "topic": topic,

            "result": result

        })

        with open(self.file, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )


    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)


    def latest(self, amount=5):

        memory = self.load()

        return memory[-amount:]


memory = MemoryEngine()
