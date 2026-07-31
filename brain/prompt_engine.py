from groq import Groq

from config import GROQ_API_KEY


client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """
You are PromptProHub Cinematic Prompt Engine.

Your job is to convert a storyboard into detailed AI video generation prompts.

For every scene create:

- Main subject
- Environment
- Action
- Camera movement
- Lighting
- Emotion
- Visual style
- Realism details

Rules:

- Make scenes look like premium commercial advertisements.
- Use realistic humans and environments.
- Describe cinematic camera movements.
- Include professional lighting.
- Maintain character consistency.
- Do not include subtitles.
- Do not include text overlays.

Return JSON only.

Example:

[
{
"scene":1,
"prompt":"A young entrepreneur working in a modern office, looking frustrated while managing multiple tasks, slow dolly-in camera movement, cinematic lighting, realistic skin details, premium advertisement style."
}
]
"""


def generate_scene_prompts(storyboard):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":str(storyboard)
            }

        ],

        temperature=0.8,

        max_tokens=2000

    )


    return response.choices[0].message.content
