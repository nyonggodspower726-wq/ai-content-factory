from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

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

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": str(marketing_plan)
            }

        ],

        temperature=0.8,

        max_tokens=800

    )

    return response.choices[0].message.content
