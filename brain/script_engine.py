from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Script AI.

You create premium short-form scripts designed to sell digital products.

Requirements:

- Hook in first 3 seconds
- Keep viewers engaged
- Build curiosity
- Teach something useful
- Naturally introduce the product
- End with a strong CTA

Length:
30–60 seconds.

Return JSON only.

Example:

{
"title":"",
"hook":"",
"script":"",
"cta":"",
"estimated_duration":"45 seconds"
}
"""


def generate_script(project):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":str(project)
            }

        ],

        temperature=0.8,

        max_tokens=2000

    )

    return response.choices[0].message.content
