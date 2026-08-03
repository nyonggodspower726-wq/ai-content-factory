from brain.ai_router import ask_ai
import json


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
]
"""


def generate_scene_prompts(storyboard):

    prompt = f"""
{SYSTEM_PROMPT}

Storyboard:

{storyboard}
"""

    raw = ask_ai(prompt)

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:

        scenes = json.loads(raw)

        scenes = scenes[:6]

        print(f"Scene prompts created: {len(scenes)}")

        return scenes

    except Exception as e:

        print("=" * 60)
        print("Prompt Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        return [
            {
                "scene": 1,
                "prompt": str(raw)
            }
        ]
