from brain.ai_router import ask_ai


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

    prompt = f"""
{SYSTEM_PROMPT}

Create a professional AI commercial plan for:

{topic}
"""

    return ask_ai(prompt)
