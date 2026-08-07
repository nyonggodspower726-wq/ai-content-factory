from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Audience AI.

Your job is to identify the perfect audience.

Return ONLY valid JSON.
No markdown.
No explanations.

Determine:

1. Primary audience
2. Secondary audience
3. Experience level
4. Biggest pain
5. Biggest desire
6. Buying intent
7. Income level
8. Content style
9. Best platform

Format:

{
"primary_audience":"Freelancers",
"secondary_audience":"Business Owners",
"experience":"Beginner",
"pain":"Writing poor AI prompts",
"desire":"Save time and earn more",
"buying_intent":"High",
"income":"Medium",
"content_style":"Educational",
"platform":"YouTube Shorts"
}
"""


def clean_json(text):

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        text = text[start:end + 1]

    return text



def audience_plan(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Analyse the audience for:

{topic}
"""


    try:

        response = ask_ai(prompt)

        response = clean_json(
            response
        )


        return json.loads(
            response
        )


    except Exception as e:


        print("=" * 60)
        print("AUDIENCE JSON ERROR")
        print("=" * 60)

        print(e)


        print("Using fallback audience")


        return {

            "primary_audience": "AI users",

            "secondary_audience": "Creators and freelancers",

            "experience": "Beginner",

            "pain": "Low productivity and lack of AI skills",

            "desire": "Save time and grow faster",

            "buying_intent": "Medium",

            "income": "Unknown",

            "content_style": "Educational",

            "platform": "YouTube Shorts"

        }
