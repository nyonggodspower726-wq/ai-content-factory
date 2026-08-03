from brain.ai_router import ask_ai
import json


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

Example:

{
    "scenes":[
        {
            "scene":1,
            "purpose":"Hook",
            "visuals":"Freelancer overwhelmed with work",
            "camera":"Close-up",
            "emotion":"Stress",
            "duration":"5s"
        },
        {
            "scene":2,
            "purpose":"Problem",
            "visuals":"Hours wasted writing prompts",
            "camera":"Tracking",
            "emotion":"Frustration",
            "duration":"6s"
        }
    ]
}
"""


def create_storyboard(plan):

    prompt = f"""
{SYSTEM_PROMPT}

Marketing Plan:

{plan}
"""

    result = ask_ai(prompt)

    try:

        return json.loads(result)

    except Exception:

        print("=" * 60)
        print("Storyboard Engine returned non-JSON.")
        print("Returning raw response.")
        print("=" * 60)

        return {
            "raw_response": result
        }
