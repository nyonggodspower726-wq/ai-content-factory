from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Cinematic Image Prompt Engine.

Your mission is to create premium cinematic AI image prompts
for FLUX and other AI image models.

The images will later be animated into short-form videos.

Main audience:

- Freelancers
- Content Creators
- Business Owners
- Digital Marketers
- AI Users

Rules:

• Maximum 8 scenes.
• Each scene must be one cinematic image.
• Every image should look like a Netflix documentary,
  Apple commercial or luxury brand advertisement.
• Every prompt must include:

- subject
- environment
- camera angle
- composition
- lighting
- emotion
- realistic details
- cinematic quality
- vertical 9:16

Always include:

ultra realistic,
cinematic lighting,
professional photography,
masterpiece,
highly detailed,
8K,
depth of field,
volumetric lighting,
sharp focus,
premium commercial quality.

Avoid:

- cartoons
- anime
- blurry
- low quality
- text
- watermark
- logo

Return ONLY valid JSON.

Example:

[
    {
        "scene":1,
        "prompt":"Ultra realistic cinematic portrait of a young entrepreneur working on a glowing laptop in a luxury modern office, dramatic golden-hour lighting, shallow depth of field, professional commercial photography, masterpiece, highly detailed, 8K, vertical 9:16."
    }
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

        if not isinstance(scenes, list):
            raise Exception("Expected a JSON list.")

        scenes = scenes[:8]

        print(
            f"Cinematic image prompts created: {len(scenes)}"
        )

        return scenes

    except Exception as e:

        print("=" * 60)
        print("PROMPT ENGINE FAILED")
        print("=" * 60)
        print(e)

        return [

            {
                "scene": 1,
                "prompt":
                "Ultra realistic cinematic portrait of a young freelancer using AI on a glowing laptop inside a luxury modern workspace, warm golden-hour lighting, dramatic shadows, shallow depth of field, premium commercial photography, masterpiece, highly detailed, volumetric lighting, 8K, vertical 9:16."
            },

            {
                "scene": 2,
                "prompt":
                "Close-up of AI-generated content appearing on multiple floating holographic screens in a futuristic office, cinematic lighting, realistic reflections, premium advertising style, masterpiece, highly detailed, 8K, vertical 9:16."
            }

     ]
