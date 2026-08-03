from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Quality AI.

Your job is to inspect every production before it is rendered.

Review the project and score it from 1–100.

Check:

1. Hook strength
2. Viewer retention
3. Emotional impact
4. Marketing effectiveness
5. CTA strength
6. Story flow
7. SEO quality
8. Overall quality

If weaknesses exist:

- Explain them.
- Suggest improvements.

Return JSON only.

Example:

{
  "score":94,
  "approved":true,
  "strengths":[
    "Excellent hook",
    "Strong curiosity",
    "Good CTA"
  ],
  "weaknesses":[
    "Scene 4 too long"
  ],
  "recommendations":[
    "Shorten scene 4 by 2 seconds"
  ]
}
"""


def quality_check(project):

    prompt = f"""
{SYSTEM_PROMPT}

Review this production:

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
        print("Quality Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        return {
            "score": 0,
            "approved": False,
            "strengths": [],
            "weaknesses": [
                "AI returned invalid JSON."
            ],
            "recommendations": [
                "Retry quality inspection."
            ],
            "raw_response": raw
        }
