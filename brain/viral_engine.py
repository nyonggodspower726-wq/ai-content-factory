from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Viral AI.

You are an expert in:

- YouTube Shorts
- TikTok
- Instagram Reels
- Facebook Reels

Evaluate every video idea.

Return JSON only.

Score:

1. Hook Score
2. Curiosity Score
3. Retention Score
4. Emotional Score
5. Shareability
6. Conversion Score
7. Viral Score (0-100)

Also give:

- Biggest weakness
- Biggest strength
- Three improvements

Example:

{
"hook":95,
"curiosity":91,
"retention":88,
"emotion":90,
"shareability":87,
"conversion":96,
"viral_score":92,
"strength":"Excellent curiosity",
"weakness":"CTA too weak",
"improvements":[
"Strengthen opening hook",
"Shorten middle section",
"Move CTA earlier"
]
}
"""


def evaluate_video(plan):

    prompt = f"""
{SYSTEM_PROMPT}

Video Plan:

{plan}
"""

    raw = ask_ai(prompt)

    raw = raw.replace("```json", "")
    raw = raw.replace("```", "")
    raw = raw.strip()

    try:

        return json.loads(raw)

    except Exception as e:

        print("=" * 60)
        print("Viral Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        return {
            "viral_score": 0,
            "strength": "Unknown",
            "weakness": "AI returned invalid JSON",
            "improvements": [],
            "raw_response": raw
        }
