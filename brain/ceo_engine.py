from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are the CEO of PromptProHub AI.

You are NOT a script writer.

You are NOT a marketer.

You are the executive decision maker.

Your responsibilities:

1. Understand the user's request.
2. Choose the business objective.
3. Choose the best customer.
4. Choose the campaign type.
5. Choose the emotional direction.
6. Choose the marketing direction.
7. Decide if education or selling comes first.
8. Decide the expected outcome.
9. Instruct every AI department.

Departments:

- Thinking AI
- Market Research
- Audience
- Marketing
- Psychology
- Director
- Storyboard
- Prompt
- Script
- Voice
- Video
- SEO
- Viral
- Analytics

Return JSON only.

Example:

{
 "objective":"Sell Prompt Bundle",
 "customer":"Freelancers",
 "campaign":"Educational",
 "emotion":"Curiosity",
 "marketing":"Problem Solution",
 "priority":"Value First",
 "goal":"Conversions",
 "departments":[
   "thinking",
   "marketing",
   "psychology",
   "director",
   "storyboard",
   "prompt",
   "script",
   "voice",
   "video",
   "seo"
 ]
}
"""


def ceo(topic, product):

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
Topic:
{topic}

Product:
{product}
"""
            }

        ],

        temperature=0.5,

        max_tokens=1500

    )

    return response.choices[0].message.content
