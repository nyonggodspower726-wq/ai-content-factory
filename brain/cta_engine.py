from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub AI Conversion Director.

Your ONLY job is to create HIGH-CONVERTING Call-To-Actions.

The CTA must sound like the ending of a premium YouTube documentary.

Audience:
- Freelancers
- Business Owners
- Content Creators
- Digital Marketers
- AI Users

Every CTA should naturally mention PromptProHub.

Whenever appropriate, naturally mention:

PromptProHub.com

Never force it.

Never sound salesy.

Psychology:

• Curiosity
• Authority
• Emotion
• FOMO
• Scarcity
• Future pacing

Avoid:

Like and Subscribe
Comment Below
Thanks For Watching
Generic YouTube endings

Generate 15 DIFFERENT CTAs.

Each CTA should feel unique.

Examples:

"If you're serious about using AI to grow faster, PromptProHub has everything you need. Visit PromptProHub.com and start today."

"The difference between watching and succeeding is taking action. Explore PromptProHub.com before your competitors do."

"One prompt can save hours of work. Imagine what hundreds can do. Discover PromptProHub today."

Return ONLY JSON.

{
    "cta":[
        "...",
        "...",
        "..."
    ]
}
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
            print("PROMPTPROHUB CTA ENGINE")
            print("=" * 60)
            print(f"Generated {len(ideas)} AI CTAs")
            print("=" * 60)

            return ideas

    except Exception as e:

        print("=" * 60)
        print("CTA ENGINE FAILED")
        print("=" * 60)
        print(e)

    print("=" * 60)
    print("USING CTA FALLBACK")
    print("=" * 60)

    return [

        "Ready to work smarter instead of harder? Visit PromptProHub.com and unlock AI tools built for creators.",

        "Every expert started with one decision. Make yours today at PromptProHub.com.",

        "Don't let your competitors discover these AI tools before you do. Visit PromptProHub.com.",

        "One great prompt can save hours. Imagine having hundreds. Explore PromptProHub today.",

        "If you're serious about growing with AI, PromptProHub was built for you.",

        "The future belongs to creators who use AI. Become one of them with PromptProHub.",

        "Your next breakthrough could start with a single prompt. Visit PromptProHub.com today.",

        "Work faster. Create better. Grow bigger. Start with PromptProHub.",

        "The smartest creators don't work harder—they work smarter with AI. Join them at PromptProHub.",

        "This is only the beginning. Discover what's possible at PromptProHub.com."

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
