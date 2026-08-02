from groq import Groq
from config import GROQ_API_KEY
import json


client = Groq(
    api_key=GROQ_API_KEY
)


SYSTEM_PROMPT = """
You are PromptProHub Cinematic Prompt Engine.

Convert a storyboard into AI video generation prompts.

STRICT RULES:

- Generate EXACTLY 6 scenes.
- Never generate more than 6 scenes.
- Each scene is one cinematic shot.
- Each scene is suitable for a short-form video.

Focus only on PromptProHub products:

- AI prompt bundles
- AI tools
- Freelancer productivity
- Content creators
- Digital marketers
- Business owners

Do not create unrelated content.

Each scene must include:

- scene number
- prompt

Return ONLY a JSON array.

Example:

[
 {
  "scene":1,
  "prompt":"A freelancer using AI tools in a modern office, cinematic camera movement, realistic lighting, premium advertisement style."
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

        temperature=0.4,

        max_tokens=1500

    )


    raw = response.choices[0].message.content


    try:

        scenes = json.loads(raw)


        # HARD SAFETY LIMIT
        scenes = scenes[:6]


        print(
            f"Scene prompts created: {len(scenes)}"
        )


        return scenes


    except Exception as e:

        print(
            "Scene JSON parsing failed:"
        )

        print(e)


        # fallback
        return [
            {
                "scene":1,
                "prompt":str(raw)
            }
        ]
