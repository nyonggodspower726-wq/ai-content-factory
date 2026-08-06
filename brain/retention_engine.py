from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub Retention Engine.

Your ONLY job is to increase watch time.

Think like:

• MrBeast
• Netflix
• Alex Hormozi

Never let viewers get bored.

Every 5–10 seconds create another reason to keep watching.

Use:

• Open loops
• Curiosity
• Suspense
• Pattern interrupts
• Future payoff
• Surprise
• Emotion

Return ONLY JSON.

Example

{
  "retention":[
      "But here's where everything changed...",
      "What happened next shocked me...",
      "Don't skip this part...",
      "The last one is unbelievable..."
  ]
}

Never explain.

Return JSON only.
"""


def generate_retention(topic):

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

        ideas = data.get("retention", [])

        if ideas:

            print("=" * 60)
            print("RETENTION ENGINE")
            print("=" * 60)
            print(f"Generated {len(ideas)} retention hooks.")
            print("=" * 60)

            return ideas

    except Exception as e:

        print(e)

    print("=" * 60)
    print("Using Retention fallback")
    print("=" * 60)

    return [

        "But that's not even the best part...",

        "Wait until you see what happens next...",

        "This is where everything changes...",

        "Almost nobody knows this part...",

        "Here's the mistake everyone makes...",

        "The last one surprised me the most...",

        "This completely changed my opinion...",

        "Don't skip this part...",

        "The next step is the real secret...",

        "You won't expect what comes next..."

    ]


def choose_retention(topic):

    ideas = generate_retention(topic)

    selected = random.choice(ideas)

    print("=" * 60)
    print("SELECTED RETENTION")
    print("=" * 60)
    print(selected)
    print("=" * 60)

    return selected
