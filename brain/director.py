from brain.ai_router import ask_ai
import json


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

Example:

{
    "video_style":"Cinematic",
    "hook":"Strong Curiosity",
    "emotion":"Excitement",
    "scene_count":6,
    "camera_style":"Dynamic",
    "music":"Epic",
    "color_grading":"High Contrast",
    "cta":"Download the Prompt Bundle"
}
"""


def create_director_plan(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Create a professional AI commercial plan for:

{topic}
"""

    result = ask_ai(prompt)

    try:

        return json.loads(result)

    except Exception:

        print("=" * 60)
        print("Director Engine returned non-JSON.")
        print("Returning raw response.")
        print("=" * 60)

        return {
            "raw_response": result
        }
