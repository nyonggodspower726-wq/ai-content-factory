from brain.ai_router import ask_ai


SYSTEM_PROMPT = """
You are PromptProHub Psychology AI.

Your purpose is to maximize viewer retention and conversions.

For every marketing plan determine:

1. Opening emotion
2. Curiosity trigger
3. Trust builder
4. Desire trigger
5. Fear of missing out
6. Viewer reward
7. Best CTA timing

Return JSON only.

Example:

{
"opening_emotion":"",
"curiosity":"",
"trust":"",
"desire":"",
"fomo":"",
"reward":"",
"cta_time":""
}
"""


def psychology_plan(marketing_plan):

    prompt = f"""
{SYSTEM_PROMPT}

Marketing Plan:

{marketing_plan}
"""

    return ask_ai(prompt)
