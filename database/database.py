import os
import json
from datetime import datetime


class Database:

    def __init__(self):
        os.makedirs("storage", exist_ok=True)

        self.file = "storage/projects.json"


    def save(self, project):

        try:

            data = []

            if os.path.exists(self.file):

                with open(self.file, "r") as f:
                    data = json.load(f)


            project["saved_at"] = str(datetime.now())

            data.append(project)


            with open(self.file, "w") as f:
                json.dump(
                    data,
                    f,
                    indent=4,
                    default=str
                )


            print("Database saved")


        except Exception as e:

            print(
                "Database error:",
                e
            )



database = Database()
