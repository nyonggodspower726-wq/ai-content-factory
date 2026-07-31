from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"Create marketing strategy for {topic}"
            }

        ],

        temperature=0.9,

        max_tokens=1000

    )

    return response.choices[0].message.content
