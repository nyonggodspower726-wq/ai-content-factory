from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Marketing AI.

Your job is NOT to write scripts.

Your job is to make videos SELL.

For every topic create:

1. Target Audience
2. Biggest Pain Point
3. Biggest Desire
4. Hook Strategy
5. Emotional Trigger
6. Curiosity Gap
7. Social Proof Idea
8. Urgency Strategy
9. CTA Strategy

Return JSON only.

Example:

{
"audience":"",
"pain":"",
"desire":"",
"hook":"",
"emotion":"",
"curiosity":"",
"social_proof":"",
"urgency":"",
"cta":""
}
"""


def marketing_plan(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Create marketing strategy for:

{topic}
"""

    result = ask_ai(prompt)

    try:

        return json.loads(result)

    except Exception:

        print("=" * 60)
        print("Marketing Engine returned non-JSON.")
        print("Returning raw response.")
        print("=" * 60)

        return {
            "raw_response": result
        }
