import json
import os

from config import (
    BRAND_NAME,
    WEBSITE_URL,
)


class BrandEngine:

    def __init__(self):

        self.brand = {

            "brand_name": BRAND_NAME,

            "website": WEBSITE_URL,

            "mission":
            "Help freelancers, creators, marketers and business owners work faster using premium AI prompts.",

            "tone":
            "Professional, premium, trustworthy and educational.",

            "target_audience": [

                "Freelancers",

                "Digital Marketers",

                "Business Owners",

                "Content Creators",

                "Students",

                "Entrepreneurs"

            ],

            "brand_colors": [

                "Blue",

                "White",

                "Black"

            ],

            "cta":
            "Visit PromptProHub to download premium AI prompts."

        }


    def get_brand(self):

        return self.brand


    def export(self, path="brain/brand.json"):

        os.makedirs("brain", exist_ok=True)

        with open(path, "w") as f:

            json.dump(

                self.brand,

                f,

                indent=4

            )

        return path


brand = BrandEngine()
