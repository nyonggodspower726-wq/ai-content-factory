from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Story Splitter.

Your job is to convert a narration into visual scenes.

Rules:

- Create between 10 and 12 scenes.
- Every scene should last about 4–5 seconds.
- Each scene should describe ONE visual moment.
- Keep the story flowing naturally.
- Return ONLY valid JSON.

Format:

[
    {
        "scene":1,
        "description":"Young entrepreneur working on a laptop in a modern office."
    },
    {
        "scene":2,
        "description":"Close-up of AI generating content on a computer screen."
    }
]
"""


def split_story(script):

    prompt = f"""
{SYSTEM_PROMPT}

Narration:

{script}
"""

    try:

        response = ask_ai(prompt)

        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        scenes = json.loads(response)

        if not isinstance(scenes, list):
            raise Exception("Invalid response.")

        print("=" * 60)
        print(f"Generated {len(scenes)} story scenes")
        print("=" * 60)

        return scenes

    except Exception as e:

        print("=" * 60)
        print("STORY SPLITTER FAILED")
        print("=" * 60)
        print(e)

        # Fallback scenes
        return [
            {"scene": 1, "description": "Professional working on a laptop."},
            {"scene": 2, "description": "Close-up of an AI dashboard."},
            {"scene": 3, "description": "Business owner planning ideas."},
            {"scene": 4, "description": "Digital marketer analyzing results."},
            {"scene": 5, "description": "Content creator editing on a computer."},
            {"scene": 6, "description": "Modern office workspace."},
            {"scene": 7, "description": "Team collaborating on AI projects."},
            {"scene": 8, "description": "Successful entrepreneur smiling."},
            {"scene": 9, "description": "PromptProHub website on a laptop."},
            {"scene": 10, "description": "Call to action with workspace background."}
  ]
