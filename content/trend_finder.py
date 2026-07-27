# content/trend_finder.py

import random

TOPICS = [
    "5 ChatGPT prompts every business owner should know",
    "3 AI tools that save hours every day",
    "How freelancers use AI to make more money",
    "Best AI prompts for marketers",
    "AI mistakes beginners should avoid",
    "How to grow your business with AI",
    "Top AI websites you should bookmark",
    "Why every creator needs AI prompts"
]

def get_trending_topic():
    """
    Returns one topic for the next video.
    Later this will be replaced with real trending-topic detection.
    """
    return random.choice(TOPICS)
