from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Creative Director and Copywriter of PromptProHub AI.

You combine the thinking of:

• Eugene Schwartz
• Gary Halbert
• David Ogilvy
• Alex Hormozi
• Russell Brunson
• MrBeast

Your mission is to produce viral, premium sales scripts.

The script must:

• Stop scrolling immediately
• Trigger curiosity
• Build emotion
• Create trust
• Sell naturally
• Increase conversions

Rules

Never begin with:

"Today..."
"Welcome..."
"In this video..."

Instead immediately create a pattern interrupt.

Structure

1. Pattern Interrupt
2. Hook
3. Problem
4. Agitate
5. Solution
6. Product
7. Benefits
8. Offer
9. Urgency
10. CTA

Video length:

30–60 seconds.

Return VALID JSON ONLY.

Example:

{

"title":"",

"hook":"",

"script":"",

"cta":"",

"estimated_duration":"45 seconds",

"visual_style":"cinematic luxury",

"music_mood":"inspirational",

"voice_style":"confident",

"color_theme":"warm premium"

}

Return JSON only.
"""


def generate_script(project):

    prompt = f"""
{SYSTEM_PROMPT}

PROJECT

{project}

Create the highest converting script possible.
"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:

        data = json.loads(response)

        data.setdefault("visual_style", "cinematic luxury")
        data.setdefault("music_mood", "inspirational")
        data.setdefault("voice_style", "confident")
        data.setdefault("color_theme", "warm premium")

        return data

    except Exception as e:

        print("=" * 60)
        print("SCRIPT ENGINE JSON ERROR")
        print(e)
        print("=" * 60)

        print(response)

        return {

            "title": "Stop Wasting Time With AI",

            "hook": "99% of people are using AI completely wrong.",

            "script":
            "99% of people ask AI basic questions and wonder why they get average results. The top creators use engineered prompts that save hours, generate better content and attract more customers. PromptProHub gives you the exact prompt systems professionals use so you can stop guessing and start creating faster.",

            "cta":
            "Get instant access to PromptProHub today.",

            "estimated_duration":
            "45 seconds",

            "visual_style":
            "cinematic luxury",

            "music_mood":
            "inspirational",

            "voice_style":
            "confident",

            "color_theme":
            "warm premium"

        }
