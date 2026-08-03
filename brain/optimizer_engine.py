from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Optimizer AI.

Your job is to improve an already-generated project.

Optimize:

1. Hook
2. Viewer retention
3. Story flow
4. Emotional impact
5. Curiosity
6. Marketing
7. CTA
8. SEO friendliness

Do NOT rewrite everything.

Improve only weak parts.

Return JSON only.

Example:

{
  "optimized": true,
  "changes": [
    "Improved hook",
    "Stronger CTA",
    "Better curiosity"
  ],
  "project": {}
}
"""


def optimize(project):

    prompt = f"""
{SYSTEM_PROMPT}

Optimize this project:

{project}
"""

    raw = ask_ai(prompt)

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:

        return json.loads(raw)

    except Exception as e:

        print("=" * 60)
        print("Optimizer Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        return {
            "optimized": False,
            "changes": [
                "Optimization failed."
            ],
            "project": project,
            "raw_response": raw
        }
