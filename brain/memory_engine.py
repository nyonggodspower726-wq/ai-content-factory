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

    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)

    def remember(self, project):

        memory = self.load()

        memory.append({

            "time": datetime.now().isoformat(),

            "topic": project.get("topic"),

            "status": project.get("status"),

            "decision": project.get("decision"),

            "viral": project.get("viral"),

            "seo": project.get("seo")

        })

        # Keep only latest 1000 memories
        memory = memory[-1000:]

        with open(self.file, "w") as f:

            json.dump(
                memory,
                f,
                indent=4
            )

    # ==========================================
    # Compatibility with older modules
    # ==========================================
    def save(self, project):
        """
        Older parts of the project call:

            memory.save(project)

        Redirect them to remember().
        """

        return self.remember(project)

    def latest(self, amount=5):

        memory = self.load()

        return memory[-amount:]

    def search(self, keyword):

        keyword = keyword.lower()

        results = []

        for item in self.load():

            topic = str(
                item.get("topic", "")
            ).lower()

            if keyword in topic:

                results.append(item)

        return results

    def total(self):

        return len(self.load())

    def clear(self):

        with open(self.file, "w") as f:

            json.dump([], f)


memory = MemoryEngine()
