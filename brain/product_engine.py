from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"Recommend the best PromptProHub product for: {topic}"
            }

        ],

        temperature=0.7,

        max_tokens=1200

    )

    return response.choices[0].message.content
