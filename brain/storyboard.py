from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Executive Storyboard Director of PromptProHub AI.

You think like:

• Apple Commercial Team
• Nike Commercial Team
• MrBeast
• Netflix Trailer Editors
• Hollywood Storyboard Artists

Your mission is to convert a marketing strategy into a HIGH-CONVERTING cinematic storyboard.

Rules:

• Every scene MUST increase curiosity.
• Every scene must push the viewer toward buying.
• Never waste a scene.
• Maximum 8 scenes.
• Every scene must have a purpose.

For EVERY scene determine:

1. Scene Number
2. Scene Purpose
3. Visual Description
4. Camera Angle
5. Camera Movement
6. Lighting
7. Emotion
8. Transition
9. Text On Screen
10. Sound Effect
11. Duration

The final scene MUST naturally sell the product.

Return VALID JSON ONLY.

Example:

{

"scenes":[

{

"scene":1,

"purpose":"Pattern Interrupt",

"visuals":"Creator staring at poor analytics while surrounded by unfinished work",

"camera_angle":"Extreme Close Up",

"camera_movement":"Fast Push In",

"lighting":"Dark Blue",

"emotion":"Shock",

"transition":"Flash Cut",

"text":"STOP SCROLLING",

"sound":"Impact Boom",

"duration":"3s"

},

{

"scene":2,

"purpose":"Problem",

"visuals":"Laptop full of unfinished projects",

"camera_angle":"Top Down",

"camera_movement":"Slow Pan",

"lighting":"Natural",

"emotion":"Frustration",

"transition":"Motion Blur",

"text":"Still doing everything manually?",

"sound":"Keyboard",

"duration":"4s"

}

]

}

Never explain.

Never use markdown.

Return JSON only.
"""


def create_storyboard(plan):

    prompt = f"""
{SYSTEM_PROMPT}

PROJECT PLAN

{plan}

Create a premium commercial storyboard.
"""

    result = ask_ai(prompt)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        return json.loads(result)

    except Exception as e:

        print("=" * 60)
        print("Storyboard Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(result)

        return {

            "scenes": [

                {

                    "scene": 1,

                    "purpose": "Pattern Interrupt",

                    "visuals": "Creator overwhelmed with work",

                    "camera_angle": "Extreme Close Up",

                    "camera_movement": "Fast Push In",

                    "lighting": "Dark Blue",

                    "emotion": "Shock",

                    "transition": "Flash Cut",

                    "text": "STOP WASTING HOURS",

                    "sound": "Impact Boom",

                    "duration": "3s"

                },

                {

                    "scene": 2,

                    "purpose": "Problem",

                    "visuals": "Multiple unfinished projects",

                    "camera_angle": "Top Down",

                    "camera_movement": "Slow Pan",

                    "lighting": "Natural",

                    "emotion": "Frustration",

                    "transition": "Motion Blur",

                    "text": "Still creating content manually?",

                    "sound": "Keyboard",

                    "duration": "4s"

                },

                {

                    "scene": 3,

                    "purpose": "Solution",

                    "visuals": "PromptProHub dashboard appearing",

                    "camera_angle": "Front",

                    "camera_movement": "Zoom In",

                    "lighting": "Bright",

                    "emotion": "Relief",

                    "transition": "Smooth Fade",

                    "text": "PromptProHub does it faster",

                    "sound": "Whoosh",

                    "duration": "4s"

                },

                {

                    "scene": 4,

                    "purpose": "Call To Action",

                    "visuals": "Product with glowing button",

                    "camera_angle": "Hero Shot",

                    "camera_movement": "Slow Push",

                    "lighting": "Premium Gold",

                    "emotion": "Excitement",

                    "transition": "Logo Reveal",

                    "text": "Get Instant Access",

                    "sound": "Cinematic Rise",

                    "duration": "4s"

                }

            ]

    }
