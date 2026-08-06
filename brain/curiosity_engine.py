from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub Curiosity Engine.

Your ONLY job is to create powerful curiosity gaps.

Your output must make people stop scrolling.

Think like:

MrBeast
Alex Hormozi
Netflix Trailers
Apple Keynotes

Rules:

Generate 15 curiosity statements.

Do NOT explain everything.

Leave an unanswered question.

Create emotional tension.

Avoid:

Welcome...
Today...
In this video...
Top 10...
Guide...
Tutorial...

Instead use:

Nobody expected...

What happened next...

I couldn't believe...

This changed everything...

The biggest mistake...

The secret...

The hidden truth...

Return ONLY JSON.

Example:

{
    "curiosity":[
        "Nobody expected what happened next.",
        "One mistake changes everything.",
        "The truth isn't what you think."
    ]
}
"""


def generate_curiosity(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Topic:

{topic}
"""

    try:

        response = ask_ai(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(response)

        ideas = data.get("curiosity", [])

        if ideas:

            print("=" * 60)
            print("CURIOSITY ENGINE")
            print("=" * 60)
            print(f"Generated {len(ideas)} curiosity ideas.")
            print("=" * 60)

            return ideas

    except Exception as e:

        print(e)

    print("=" * 60)
    print("Using Curiosity fallback")
    print("=" * 60)

    return [

        "Nobody expected what happened next.",

        "The biggest mistake changes everything.",

        "This secret completely surprised me.",

        "Most people never discover this.",

        "I wish someone told me this sooner.",

        "The truth is completely different.",

        "You're probably making this mistake.",

        "Everything changed after this.",

        "Almost nobody notices this.",

        "This one decision changed everything."

    ]


def choose_curiosity(topic):

    ideas = generate_curiosity(topic)

    curiosity = random.choice(ideas)

    print("=" * 60)
    print("SELECTED CURIOSITY")
    print("=" * 60)
    print(curiosity)
    print("=" * 60)

    return curiosity
