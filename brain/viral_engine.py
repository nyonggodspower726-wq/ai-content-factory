from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Viral AI.

You are an expert in:

- YouTube Shorts
- TikTok
- Instagram Reels
- Facebook Reels

Evaluate every video idea.

Return JSON only.

Score:

1. Hook Score
2. Curiosity Score
3. Retention Score
4. Emotional Score
5. Shareability
6. Conversion Score
7. Viral Score (0-100)

Also give:

- Biggest weakness
- Biggest strength
- Three improvements

Example:

{
"hook":95,
"curiosity":91,
"retention":88,
"emotion":90,
"shareability":87,
"conversion":96,
"viral_score":92,
"strength":"...",
"weakness":"...",
"improvements":[
"...",
"...",
"..."
]
}
"""


def evaluate_video(plan):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":str(plan)
            }

        ],

        temperature=0.7,

        max_tokens=1200

    )

    return response.choices[0].message.content
