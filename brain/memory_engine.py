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
    # Compatibility with old and new modules
    # ==========================================
    def save(self, *args):

        """
        Supports both:

            memory.save(project)

        and

            memory.save(key, value)
        """

        if len(args) == 1:

            project = args[0]

            if isinstance(project, dict):

                return self.remember(project)

            return

        elif len(args) == 2:

            key, value = args

            memory = self.load()

            memory.append({

                "time": datetime.now().isoformat(),

                str(key): value

            })

            memory = memory[-1000:]

            with open(self.file, "w") as f:

                json.dump(
                    memory,
                    f,
                    indent=4
                )

            return

        else:

            raise TypeError(
                "save() expects either 1 or 2 arguments."
            )

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
