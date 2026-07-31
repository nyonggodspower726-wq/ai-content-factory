from groq import Groq

from config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """
You are the Director of PromptProHub AI Studio.

You never write a full script.

You plan videos.

Return JSON only.

You decide:

1. Video style
2. Hook
3. Emotion
4. Number of scenes
5. Camera style
6. Music mood
7. Colour grading
8. Call to action
"""


def create_director_plan(topic):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content":
                f"Create a professional AI commercial plan for: {topic}"
            }

        ],

        temperature=0.8,

        max_tokens=800

    )

    return response.choices[0].message.content
