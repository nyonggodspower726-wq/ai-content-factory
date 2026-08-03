from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Offer AI.

Your job is to create irresistible offers.

Return JSON only.

Determine:

1. Best Offer
2. Product Bundle
3. Bonus
4. Scarcity
5. Urgency
6. Value Proposition
7. CTA

Example:

{
"offer":"",
"bundle":"",
"bonus":"",
"scarcity":"",
"urgency":"",
"value":"",
"cta":""
}
"""


def create_offer(product, audience):

    prompt = f"""
{SYSTEM_PROMPT}


Product:

{product}


Audience:

{audience}


Create the strongest possible offer.
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


        return {

            "offer": "Premium AI Productivity Bundle",

            "bundle": "AI prompts + workflows + guides",

            "bonus": "Free AI productivity checklist",

            "scarcity": "Limited launch access",

            "urgency": "Early users get bonuses",

            "value": "Save time and increase productivity",

            "cta": "Get access now"

        }
