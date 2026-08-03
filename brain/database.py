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


    def load(self):

        with open(self.database, "r") as f:

            return json.load(f)


    def save(self, project):

        data = self.load()

        project["created"] = datetime.now(
            ZoneInfo("Africa/Lagos")
        ).strftime("%Y-%m-%d %H:%M:%S")

        project["id"] = len(data) + 1

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


    def latest(self):

        data = self.load()

        if not data:

            return None

        return data[-1]


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


    def count(self):

        return len(self.load())


    def report(self):

        print("=" * 60)
        print("DATABASE REPORT")
        print("=" * 60)

        print(f"Projects Stored : {self.count()}")

        latest = self.latest()

        if latest:

            print(f"Latest Project : {latest.get('topic')}")

        print("=" * 60)


    def clear(self):

        with open(self.database, "w") as f:

            json.dump([], f, indent=4)


database = ProductionDatabase()
