# content/hashtag_generator.py

import random

HASHTAGS = [
    "#AI",
    "#ChatGPT",
    "#AITools",
    "#Productivity",
    "#Business",
    "#DigitalProducts",
    "#Freelancer",
    "#Marketing",
    "#Entrepreneur",
    "#SideHustle",
    "#OnlineBusiness",
    "#PromptEngineering"
]

def generate_hashtags():
    """
    Returns 5 random hashtags.
    """
    return " ".join(random.sample(HASHTAGS, 5))
