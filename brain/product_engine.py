from brain.ai_router import ask_ai


SYSTEM_PROMPT = """
You are PromptProHub Product AI.

Your job is to match videos with the best product.

Return JSON only.

Determine:

1. Best product
2. Product category
3. Customer level
4. Problem solved
5. Product benefits
6. Best CTA
7. Sales angle

Example:

{
"product":"",
"category":"",
"level":"",
"problem":"",
"benefits":[
"",
"",
""
],
"cta":"",
"sales_angle":""
}
"""


def recommend_product(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Recommend the best PromptProHub product for:

{topic}
"""

    return ask_ai(prompt)
