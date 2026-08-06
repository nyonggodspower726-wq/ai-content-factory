from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub CTA Engine.

Your ONLY job is to create HIGH-CONVERTING Call-To-Actions.

Think like:

• Alex Hormozi
• Russell Brunson
• Apple
• MrBeast

Rules:

Never use boring CTAs.

Avoid:

Like and Subscribe...

Thanks for watching...

Comment below...

Instead create CTAs that feel natural.

Generate 15 CTAs.

Return ONLY JSON.

Example

{
    "cta":[
        "If you're serious about growing, save this video because you'll need it later.",
        "The people who act first always win.",
        "Everything starts with one decision."
    ]
}

Return JSON only.
"""


def generate_cta(topic):

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

        ideas = data.get("cta", [])

        if ideas:

            print("=" * 60)
            print("CTA ENGINE")
            print("=" * 60)
            print(f"Generated {len(ideas)} CTAs.")
            print("=" * 60)

            return ideas

    except Exception as e:

        print(e)

    print("=" * 60)
    print("Using CTA fallback")
    print("=" * 60)

    return [

        "If you're serious about growing, don't ignore what you've just learned.",

        "The people who succeed are the ones who take action today.",

        "Save this because you'll want to come back to it later.",

        "Start applying this today and thank yourself later.",

        "Small actions today create massive results tomorrow.",

        "The next move is yours.",

        "Success always starts with one decision.",

        "Don't just watch... use this.",

        "Turn this knowledge into results.",

        "If this helped you, imagine what happens when you apply it."

    ]


def choose_cta(topic):

    ideas = generate_cta(topic)

    selected = random.choice(ideas)

    print("=" * 60)
    print("SELECTED CTA")
    print("=" * 60)
    print(selected)
    print("=" * 60)

    return selected
