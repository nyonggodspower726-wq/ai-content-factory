from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Audience AI.

Your job is to identify the perfect audience.

Return JSON only.

Determine:

1. Primary audience
2. Secondary audience
3. Experience level
4. Biggest pain
5. Biggest desire
6. Buying intent
7. Income level
8. Content style
9. Best platform

Example:

{
"primary_audience":"Freelancers",
"secondary_audience":"Business Owners",
"experience":"Beginner",
"pain":"Writing poor AI prompts",
"desire":"Save time and earn more",
"buying_intent":"High",
"income":"Medium",
"content_style":"Educational",
"platform":"YouTube Shorts"
}
"""


def analyse_audience(topic):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"Analyse audience for {topic}"
            }

        ],

        temperature=0.7,

        max_tokens=1000

    )

    return response.choices[0].message.content
