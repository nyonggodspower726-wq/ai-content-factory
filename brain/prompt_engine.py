from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Cinematic Camera Prompt Engine.

Your job is to convert a storyboard into premium AI video generation prompts.

You create prompts for:
- AI video models
- cinematic advertising
- short-form sales videos

Main topics:

- AI prompt bundles
- AI productivity tools
- freelancers
- creators
- digital marketers
- business owners


RULES:

- Generate maximum 6 scenes.
- Each scene must be a single cinematic shot.
- Each scene must feel like a premium advertisement.
- Include realistic camera direction.
- Include lighting.
- Include movement.
- Include emotion.
- Include environment details.

Avoid:
- cartoons
- low quality visuals
- random scenes
- unrelated topics


Return ONLY JSON array.

Format:

[
 {
   "scene":1,
   "prompt":"Detailed cinematic video prompt"
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


    raw = raw.replace(
        "```json",
        ""
    )

    raw = raw.replace(
        "```",
        ""
    )

    raw = raw.strip()



    try:


        scenes = json.loads(
            raw
        )


        if not isinstance(
            scenes,
            list
        ):

            raise Exception(
                "Not a list"
            )


        scenes = scenes[:6]


        print(
            f"Cinematic prompts created: {len(scenes)}"
        )


        return scenes



    except Exception as e:


        print("=" * 60)
        print("PROMPT ENGINE FAILED")
        print(e)
        print("=" * 60)



        return [

            {
                "scene": 1,

                "prompt":
                """
                A premium cinematic advertisement showing
                a freelancer discovering AI productivity tools
                in a modern workspace, realistic lighting,
                slow camera movement, professional commercial style.
                """
            }

     ]
