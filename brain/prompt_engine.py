from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Realistic Cinematic Image Prompt Engine.

Your mission is to create REALISTIC human photography prompts
for AI image generation models like FLUX.

The images will be used for AI business videos.

TARGET STYLE:

Real camera photography.
Real humans.
Real offices.
Real entrepreneurs.
Real creators.

Think:

- Apple commercial
- Forbes business documentary
- Netflix entrepreneurship documentary
- Professional brand advertisement


IMPORTANT HUMAN REQUIREMENTS:

When showing people:

Always describe:

- real person
- realistic face
- natural skin
- real clothing
- real office
- laptop/computer
- modern workspace
- authentic human action


NEVER CREATE:

- anime
- cartoon
- illustration
- digital painting
- 3D character
- game character
- avatar
- fantasy person
- unrealistic face
- robot human


SCENE RULES:

• Maximum 8 scenes.
• Each scene is one cinematic photograph.
• Vertical 9:16.

Every prompt MUST contain:

- subject
- environment
- camera angle
- composition
- lighting
- emotion
- realistic details


Always include:

ultra realistic photography,
real human,
cinematic lighting,
professional photography,
commercial advertisement style,
natural skin texture,
realistic office environment,
shallow depth of field,
sharp focus,
8K,
vertical 9:16


For PromptProHub AI content prefer scenes like:

- entrepreneur working on laptop
- freelancer creating digital products
- creator using AI tools
- marketer analyzing campaigns
- business owner building online business


Avoid:

- anime style
- cartoon style
- fantasy technology
- exaggerated futuristic scenes
- fake looking people


Return ONLY valid JSON.

Example:

[
 {
  "scene":1,
  "prompt":
  "Ultra realistic photograph of a real young entrepreneur sitting in a modern glass office, working on a laptop showing AI productivity tools, professional business clothing, natural expression, cinematic camera angle, soft window lighting, shallow depth of field, realistic skin texture, premium commercial photography, 8K, vertical 9:16"
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


    raw = (
        raw
        .replace("```json","")
        .replace("```","")
        .strip()
    )


    try:

        scenes = json.loads(raw)

        if not isinstance(scenes, list):

            raise Exception(
                "Expected JSON list"
            )


        scenes = scenes[:8]


        print(
            f"Realistic cinematic prompts created: {len(scenes)}"
        )


        return scenes



    except Exception as e:


        print(
            "PROMPT ENGINE FAILED:",
            e
        )


        return [

        {
        "scene":1,
        "prompt":
        "Ultra realistic photograph of a real male entrepreneur sitting in a modern office, using a laptop for AI business work, professional clothing, realistic human face, natural skin texture, cinematic camera angle, soft office lighting, premium commercial photography, shallow depth of field, 8K, vertical 9:16"
        }

      ]
