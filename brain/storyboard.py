from groq import Groq

from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are a professional commercial storyboard artist.

Your job is to convert a marketing plan into a cinematic storyboard.

Rules:

- Every scene must increase curiosity.
- Maximum 8 scenes.
- Every scene must describe:
    - purpose
    - visuals
    - camera
    - emotion
    - duration

The final scene MUST sell the product naturally.

Return JSON only.
"""


def create_storyboard(plan):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": str(plan)
            }

        ],

        temperature=0.8,

        max_tokens=1200

    )

    return response.choices[0].message.content
