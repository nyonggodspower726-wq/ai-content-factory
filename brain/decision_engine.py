from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Decision AI.

Your job is to make the final production decision.

You receive:

- Brand
- Trend
- Product
- Marketing
- Psychology
- Storyboard
- Viral Analysis

Return JSON only.

Decide:

1. Should this video be produced?
2. Confidence score (0-100)
3. Best publishing platform
4. Best posting time
5. Expected audience
6. Expected conversion
7. Final recommendation

Example:

{
"produce": true,
"confidence": 96,
"platform": "YouTube Shorts",
"posting_time": "18:00",
"audience": "Digital Marketers",
"conversion": "High",
"recommendation": "Publish immediately"
}
"""


def final_decision(project):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": str(project)
            }

        ],

        temperature=0.6,

        max_tokens=1200

    )

    return response.choices[0].message.content
