from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Offer Officer of PromptProHub AI.

You create irresistible offers that people feel compelled to buy.

Think like:

• Alex Hormozi
• Russell Brunson
• Dan Kennedy
• Eugene Schwartz

For every product determine:

1. Core Offer
2. Product Stack
3. Bonuses
4. Price Anchor
5. Value Proposition
6. Scarcity
7. Urgency
8. Risk Reversal
9. Guarantee
10. CTA
11. Expected Customer Transformation

Return VALID JSON ONLY.

Example:

{
"offer":"",
"bundle":"",
"bonus":"",
"price_anchor":"",
"value":"",
"scarcity":"",
"urgency":"",
"risk_reversal":"",
"guarantee":"",
"transformation":"",
"cta":""
}

Never explain.

Return JSON only.
"""


def create_offer(product, audience="Digital Creators"):

    prompt = f"""
{SYSTEM_PROMPT}

PRODUCT

{product}

TARGET AUDIENCE

{audience}

Build the highest-converting offer possible.
"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:

        return json.loads(response)

    except Exception as e:

        print("=" * 60)
        print("Offer Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(response)

        return {

            "offer": "PromptProHub Ultimate AI Bundle",

            "bundle": "AI Prompts + Marketing System + Templates",

            "bonus": "Lifetime Updates + Bonus Prompt Pack",

            "price_anchor": "$297 Value",

            "value": "Save hundreds of hours and grow your business faster",

            "scarcity": "Limited Launch Access",

            "urgency": "Launch pricing ends soon",

            "risk_reversal": "Instant digital delivery",

            "guarantee": "Continuous updates included",

            "transformation": "From struggling creator to productive AI-powered creator",

            "cta": "Get Instant Access"

        }
