from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub Hook Engine.

Your ONLY job is to write hooks that make people stop scrolling.

The hook must instantly create curiosity.

Think like:

MrBeast
Alex Hormozi
Netflix
Apple
Top TikTok creators

Rules:

Generate 15 hooks.

Maximum 2 sentences.

Never start with:

Welcome...
Today...
In this video...
Top 10...
Guide...
Tutorial...

Use patterns like:

"You've been..."

"Almost everyone..."

"I made a mistake..."

"Nobody tells you..."

"I wish I knew..."

"This changes everything..."

"If you still..."

"Stop doing..."

Return ONLY JSON.

Example:

{
    "hooks":[
        "You're making one mistake that almost everyone misses.",
        "I wish someone told me this years ago.",
        "This completely changed how I work."
    ]
}
"""


def generate_hooks(topic, angle, curiosity):

    prompt = f"""
{SYSTEM_PROMPT}

Topic:

{topic}

Viral Angle:

{angle}

Curiosity:

{curiosity}
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

        hooks = data.get("hooks", [])

        if hooks:

            print("=" * 60)
            print("HOOK ENGINE")
            print("=" * 60)
            print(f"Generated {len(hooks)} hooks.")
            print("=" * 60)

            return hooks

    except Exception as e:

        print(e)

    print("=" * 60)
    print("Using Hook fallback")
    print("=" * 60)

    return [

        f"Almost everyone gets {topic} completely wrong.",

        f"I wish someone had shown me {topic} earlier.",

        f"This completely changed how I use {topic}.",

        f"You're probably making this {topic} mistake.",

        f"Nobody talks about this part of {topic}.",

        f"If you're still doing this with {topic}, stop now.",

        f"This one discovery changed everything.",

        f"I almost ignored this... until I saw the results.",

        f"This is the hidden truth about {topic}.",

        f"Most people never notice this."

    ]


def choose_hook(topic, angle, curiosity):

    hooks = generate_hooks(
        topic,
        angle,
        curiosity
    )

    hook = random.choice(hooks)

    print("=" * 60)
    print("SELECTED HOOK")
    print("=" * 60)
    print(hook)
    print("=" * 60)

    return hook
