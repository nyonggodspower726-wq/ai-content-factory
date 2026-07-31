from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

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


def create_offer(topic):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"Create the best offer for {topic}"
            }

        ],

        temperature=0.8,

        max_tokens=1000

    )

    return response.choices[0].message.content
