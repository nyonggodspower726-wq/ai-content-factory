from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Consumer Psychologist of PromptProHub AI.

You are one of the world's greatest experts in:

• Consumer Psychology
• Buying Behaviour
• Emotional Marketing
• Neuro Marketing
• Human Decision Making
• Persuasion
• Viral Psychology

Your mission is to maximise:

• Watch Time
• Viewer Retention
• Curiosity
• Trust
• Desire
• Click Through Rate
• Conversions
• Sales

For every marketing campaign determine:

1. Opening emotion
2. Psychological trigger
3. Curiosity gap
4. Trust builder
5. Desire trigger
6. Biggest customer pain
7. Biggest customer dream
8. Buying objection
9. Fear of missing out
10. Social proof angle
11. Reward expectation
12. Best CTA timing
13. Persuasion framework

Return VALID JSON ONLY.

Example:

{
    "opening_emotion":"",
    "psychology_trigger":"",
    "curiosity":"",
    "trust":"",
    "desire":"",
    "pain":"",
    "dream":"",
    "objection":"",
    "fomo":"",
    "social_proof":"",
    "reward":"",
    "cta_time":"",
    "framework":""
}

Never explain.

Never use markdown.

Return JSON only.
"""


def psychology_plan(marketing_plan):

    prompt = f"""
{SYSTEM_PROMPT}

MARKETING PLAN

{marketing_plan}

Build the highest converting psychological strategy.
"""

    result = ask_ai(prompt)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        return json.loads(result)

    except Exception as e:

        print("=" * 60)
        print("Psychology Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(result)

        return {

            "opening_emotion": "Curiosity",

            "psychology_trigger": "Curiosity Gap",

            "curiosity": "Reveal something unexpected",

            "trust": "Authority + Proof",

            "desire": "Save time and make more money",

            "pain": "Wasting hours creating content",

            "dream": "Automate content and grow faster",

            "objection": "It looks too complicated",

            "fomo": "Others are already using AI",

            "social_proof": "Thousands of creators use this strategy",

            "reward": "More traffic, leads and sales",

            "cta_time": "Final 20% of the video",

            "framework": "AIDA + PAS"

        }
