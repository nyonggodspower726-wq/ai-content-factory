from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Script AI.

You create premium short-form scripts designed to sell digital products.

Requirements:

- Hook in first 3 seconds.
- Keep viewers engaged.
- Build curiosity.
- Teach something useful.
- Naturally introduce the product.
- End with a strong CTA.

Length:

30–60 seconds.

Return JSON only.

Example:

{
"title":"",
"hook":"",
"script":"",
"cta":"",
"estimated_duration":"45 seconds"
}
"""


def generate_script(project):

    prompt = f"""
{SYSTEM_PROMPT}

Project Information:

{project}
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


        return {

            "title": "PromptProHub AI Productivity System",

            "hook": "You are wasting hours doing tasks AI can finish in minutes.",

            "script": response,

            "cta": "Get the PromptProHub AI bundle today.",

            "estimated_duration": "45 seconds"

        }
