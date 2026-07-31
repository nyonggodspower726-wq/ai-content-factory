from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Trend AI.

Your job is to identify content opportunities.

For every niche return JSON only.

Determine:

1. Trending topics
2. Evergreen topics
3. Beginner topics
4. Advanced topics
5. High buying intent topics
6. Recommended content priority

Example:

{
"trending":[
"...",
"..."
],
"evergreen":[
"...",
"..."
],
"beginner":[
"..."
],
"advanced":[
"..."
],
"buyer_intent":[
"..."
],
"priority":"..."
}
"""


def discover_trends(niche):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": f"Analyse this niche: {niche}"
            }

        ],

        temperature=0.7,

        max_tokens=1200

    )

    return response.choices[0].message.content
