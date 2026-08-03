import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo


class ProductionDatabase:

    def __init__(self):

        self.database = "database/projects.json"

        os.makedirs("database", exist_ok=True)

        if not os.path.exists(self.database):

            with open(self.database, "w") as f:

                json.dump([], f, indent=4)

    def save(self, project):

        with open(self.database, "r") as f:

            data = json.load(f)

        project["created"] = datetime.now(
            ZoneInfo("Africa/Lagos")
        ).strftime("%Y-%m-%d %H:%M:%S")

        data.append(project)

        with open(self.database, "w") as f:

            json.dump(
                data,
                f,
                indent=4
            )

        print("=" * 60)
        print("PROJECT SAVED")
        print("=" * 60)

    def load(self):

        with open(self.database, "r") as f:

            return json.load(f)

    def latest(self):

        data = self.load()

        if len(data) == 0:

            return None

        return data[-1]

    def count(self):

        return len(self.load())

    def clear(self):

        with open(self.database, "w") as f:

            json.dump([], f)


database = ProductionDatabase()
