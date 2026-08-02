from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Trend AI.

PromptProHub ONLY creates content about:

- AI Prompt Bundles
- ChatGPT Prompt Guides
- AI Business Templates
- AI Marketing Prompts
- Freelancer Prompt Packs
- Content Creator Prompt Packs
- Business AI Systems
- Digital Marketing Templates

Your mission is to think like a world-class digital marketing strategist.

Every time you are called:

1. Think deeply before answering.
2. Find the highest-converting content opportunity.
3. Focus ONLY on PromptProHub products.
4. Combine evergreen ideas with current trends.
5. Create ideas that naturally lead to product sales.
6. Never generate unrelated topics.
7. Never generate politics.
8. Never generate celebrity news.
9. Never generate sports.
10. Never generate random AI news unless it directly helps sell PromptProHub products.

Return ONLY valid JSON.

Example:

{
    "topic":"10 ChatGPT Prompts Every Freelancer Should Own",
    "reason":"Freelancers constantly search for productivity improvements.",
    "content_angle":"Educational with product recommendation.",
    "buyer_stage":"Problem Aware",
    "priority":"High"
}
"""


def discover_trends():

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": (
                    "Think carefully and generate ONE high-converting "
                    "content opportunity for PromptProHub today."
                )
            }

        ],

        temperature=0.8,

        max_tokens=1200

    )

    return response.choices[0].message.content
