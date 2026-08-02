from brain.ai_router import ask_ai


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

    prompt = f"""
{SYSTEM_PROMPT}

Marketing Plan:

{plan}
"""

    return ask_ai(prompt)
