import json


class ConsistencyEngine:

    def __init__(self):

        self.character = {

            "gender": "young professional",

            "age": "23 years old",

            "skin": "dark skin",

            "hair": "short black hair",

            "clothes": "modern smart casual",

            "expression": "confident",

            "style": "premium commercial"
        }

        self.environment = {

            "office": "modern luxury workspace",

            "lighting": "cinematic",

            "brand_colors": "blue white black",

            "quality": "8k ultra realistic"
        }


    def apply(self, prompt):

        identity = (

            f"{self.character['gender']}, "

            f"{self.character['age']}, "

            f"{self.character['skin']}, "

            f"{self.character['hair']}, "

            f"{self.character['clothes']}, "

            f"{self.environment['office']}, "

            f"{self.environment['lighting']}, "

            f"{self.environment['quality']}"
        )

        return f"{prompt}, {identity}"


    def export(self):

        return json.dumps(

            {

                "character": self.character,

                "environment": self.environment

            },

            indent=4

        )
