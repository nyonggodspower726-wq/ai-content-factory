from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Trend Brain.

Your only job is to generate HIGHLY CLICKABLE video ideas.

Never generate boring topics.

Never generate generic titles.

Think like:

• MrBeast
• Alex Hormozi
• Ali Abdaal
• Iman Gadzhi

The goal is to maximize:

- Curiosity
- Clicks
- Shares
- Watch time

Rules:

Generate 20 UNIQUE video ideas.

Every title should create curiosity.

Avoid:

Top 10...

Best...

Guide...

Tutorial...

Welcome...

Instead use patterns like:

"I tried..."

"This mistake..."

"Nobody knows..."

"Stop doing..."

"You're wasting..."

"The truth about..."

"What happened when..."

Return ONLY valid JSON.

Example:

{
    "ideas":[
        "I tested 100 AI prompts so you don't have to",
        "You're wasting ChatGPT if you still do this",
        "Nobody told freelancers this AI trick",
        "The prompt that replaced 5 hours of work"
    ]
}
"""


def generate_trending_ideas(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Main topic:

{topic}
"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:

        data = json.loads(response)

        ideas = data.get("ideas", [])

        if ideas:

            print("=" * 60)
            print("TREND BRAIN")
            print("=" * 60)
            print(f"Generated {len(ideas)} viral ideas.")
            print("=" * 60)

            return ideas

    except Exception:

        pass

    print("=" * 60)
    print("Trend Brain fallback")
    print("=" * 60)

    return [

        "I tested 100 AI prompts so you don't have to",

        "The ChatGPT trick nobody tells freelancers",

        "You're wasting AI if you still do this",

        "The AI prompt that replaced five hours of work",

        "This AI workflow changed everything",

        "Most creators use ChatGPT the wrong way",

        "Stop asking ChatGPT basic questions",

        "The secret prompt professionals actually use",

        "I wish I knew this AI trick earlier",

        "The AI prompt that made me more productive"

    ]
