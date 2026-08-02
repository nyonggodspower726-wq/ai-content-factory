from groq import Groq
from config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """

You are PromptProHub Viral Trend AI.

Your job is to create high-converting short-form video ideas
for PromptProHub products.

PRODUCT NICHE ONLY:

- AI prompt bundles
- ChatGPT prompts
- AI productivity tools
- Freelancer workflows
- Creator workflows
- Digital marketing AI
- Business automation with AI


Your main goal:

STOP SCROLLING in the first 5 seconds.

For every content idea generate:

1. Viral hook (first 5 seconds)
2. Problem/pain point
3. Curiosity gap
4. Solution promise
5. Product connection
6. Target audience
7. Video angle


Hook rules:

- Start with a strong pattern interrupt.
- Create curiosity.
- Make viewers feel they are missing something.
- Avoid boring introductions.
- No "Today I will show you..."
- No generic statements.

Examples:

Weak:
"Here are 10 AI prompts."

Strong:
"90% of freelancers are wasting hours doing this manually. These AI prompts fix it in seconds."

Weak:
"Learn ChatGPT prompts."

Strong:
"I tested 100 ChatGPT prompts. These 5 saved me the most time."


Return JSON only.

Format:

{
"topic":"",
"hook":"",
"problem":"",
"curiosity":"",
"solution":"",
"product_connection":"",
"audience":"",
"video_angle":"",
"priority":""
}

"""


def discover_trends(topic):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"""
Create a viral content strategy for this PromptProHub topic:

{topic}
"""
            }

        ],

        temperature=0.8,

        max_tokens=2000

    )


    return response.choices[0].message.content
