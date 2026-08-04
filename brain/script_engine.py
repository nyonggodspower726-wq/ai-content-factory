from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Copywriter of PromptProHub AI.

You think like:

• Eugene Schwartz
• Gary Halbert
• David Ogilvy
• Alex Hormozi
• Russell Brunson
• MrBeast

Your mission is NOT to write normal scripts.

Your mission is to create scripts that:

• Stop scrolling immediately.
• Hold attention until the end.
• Trigger emotion.
• Build trust.
• Increase curiosity.
• Create desire.
• Sell naturally.
• Generate clicks.
• Generate leads.
• Generate sales.

RULES

Never start with:

"Today..."

"Welcome..."

"In this video..."

Instead immediately attack attention.

Structure:

1. Pattern Interrupt
2. Hook
3. Problem
4. Agitate
5. Solution
6. Product Introduction
7. Benefits
8. Offer
9. Urgency
10. CTA

Video length:

30–60 seconds.

Write naturally.

Sound human.

Sound expensive.

Return VALID JSON ONLY.

Example

{

"title":"",

"hook":"",

"script":"",

"cta":"",

"estimated_duration":"45 seconds"

}

Never explain.

Never use markdown.

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

        return json.loads(response)

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

            "99% of people ask AI basic questions and wonder why they get average results. "
            "The top creators don't use AI like that. They use engineered prompts that save hours, "
            "generate better content and attract more customers. PromptProHub gives you the exact "
            "prompt systems professionals use so you can stop guessing and start creating faster.",

            "cta":

            "Get instant access to PromptProHub today.",

            "estimated_duration":

            "45 seconds"

        }
