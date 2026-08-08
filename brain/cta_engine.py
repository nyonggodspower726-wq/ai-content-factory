from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub AI Conversion Director.

Your ONLY job is to create HIGH-CONVERTING spoken Call-To-Actions
for the END of short-form videos.

The CTA will be spoken by an AI voice.

Audience:
- Freelancers
- Business Owners
- Content Creators
- Digital Marketers
- AI Users

Every CTA should naturally mention PromptProHub when appropriate.

IMPORTANT CTA REQUIREMENTS:

Every CTA MUST contain BOTH:

1. A natural instruction to click/check the link in the bio.
2. A natural instruction to follow for more.

Use natural variations such as:

"Click the link in my bio and follow for more."

"Check the link in the bio, and follow for more AI strategies."

"If you want more tools like this, click the link in my bio and follow for more."

Do NOT make every CTA sound identical.

The CTA should sound like the natural ending of a premium
YouTube/TikTok documentary.

Psychology:
- Curiosity
- Authority
- Emotion
- FOMO
- Future pacing
- Action

Avoid:
- Like and Subscribe
- Comment Below
- Thanks For Watching
- "Please support us"
- Robotic sales language
- Excessive hype

Keep each CTA short enough to be spoken naturally.

Generate exactly 15 DIFFERENT CTAs.

Return ONLY valid JSON.

{
    "cta":[
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "..."
    ]
}
"""


def generate_cta(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Video Topic:

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

        ideas = data.get(
            "cta",
            []
        )

        if ideas:

            print("=" * 60)
            print("PROMPTPROHUB CTA ENGINE")
            print("=" * 60)

            print(
                f"Generated {len(ideas)} AI CTAs"
            )

            print("=" * 60)

            return ideas

    except Exception as e:

        print("=" * 60)
        print("CTA ENGINE FAILED")
        print("=" * 60)

        print(
            type(e).__name__
        )

        print(
            str(e)
        )


    # =====================================
    # FALLBACK CTAs
    # =====================================

    print("=" * 60)
    print("USING CTA FALLBACK")
    print("=" * 60)


    return [

        (
            "Want more AI tools like this? "
            "Click the link in my bio and follow for more."
        ),

        (
            "If you're serious about using AI to work smarter, "
            "check the link in my bio and follow for more."
        ),

        (
            "There's more waiting for you. "
            "Click the link in my bio and follow for more AI strategies."
        ),

        (
            "Ready to take your AI game further? "
            "Click the link in my bio and follow for more."
        ),

        (
            "Discover more powerful AI tools through the link in my bio, "
            "and follow for more."
        ),

        (
            "If this saved you time, imagine what's next. "
            "Click the link in my bio and follow for more."
        ),

        (
            "Your next AI breakthrough could be one click away. "
            "Check the link in my bio and follow for more."
        ),

        (
            "Want to build faster with AI? "
            "Click the link in my bio and follow for more."
        ),

        (
            "Don't stop here. "
            "Explore the link in my bio and follow for more AI tools."
        ),

        (
            "More practical AI strategies are waiting for you. "
            "Click the link in my bio and follow for more."
        )

    ]


def choose_cta(topic):

    ideas = generate_cta(
        topic
    )

    if not ideas:

        return (
            "Want more AI tools like this? "
            "Click the link in my bio and follow for more."
        )

    selected = random.choice(
        ideas
    )

    print("=" * 60)
    print("SELECTED CTA")
    print("=" * 60)

    print(
        selected
    )

    print("=" * 60)

    return selected
