from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Decision AI.

Your job is to make the final production decision.

You receive:

- Brand
- Trend
- Product
- Marketing
- Psychology
- Storyboard
- Viral Analysis

Return JSON only.

Decide:

1. Should this video be produced?
2. Confidence score (0-100)
3. Best publishing platform
4. Best posting time
5. Expected audience
6. Expected conversion
7. Final recommendation

Example:

{
"produce": true,
"confidence": 96,
"platform": "YouTube Shorts",
"posting_time": "18:00",
"audience": "Digital Marketers",
"conversion": "High",
"recommendation": "Publish immediately"
}
"""


def final_decision(project):

    prompt = f"""
{SYSTEM_PROMPT}

Project:

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
        print("Decision Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        return {
            "produce": False,
            "confidence": 0,
            "platform": "Unknown",
            "posting_time": "Unknown",
            "audience": "Unknown",
            "conversion": "Unknown",
            "recommendation": "Retry AI generation",
            "raw_response": raw
        }
