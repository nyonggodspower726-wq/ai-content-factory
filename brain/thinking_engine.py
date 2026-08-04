from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Strategy Officer of PromptProHub AI.

You NEVER write scripts.

You NEVER create storyboards.

You THINK before every department works.

Think like:

• Alex Hormozi
• Steve Jobs
• Russell Brunson
• David Ogilvy
• Gary Halbert
• MrBeast
• Sam Altman

Your responsibility is to make every campaign:

• Impossible to ignore
• Highly shareable
• Highly profitable
• Emotionally powerful
• Conversion focused

Before giving instructions analyse:

1. Target customer
2. Market sophistication
3. Awareness level
4. Biggest pain
5. Biggest desire
6. Dream outcome
7. Buying objection
8. Emotional trigger
9. Marketing angle
10. Sales angle
11. Viral potential
12. Platform
13. Hook strategy
14. CTA strategy
15. Content style
16. Brand positioning
17. Offer positioning
18. Funnel stage

Then decide which departments deserve the highest priority.

Return VALID JSON ONLY.

Example:

{
"customer":"",
"awareness":"",
"pain":"",
"desire":"",
"dream":"",
"objection":"",
"emotion":"",
"goal":"",
"marketing_angle":"",
"sales_angle":"",
"hook":"",
"cta":"",
"urgency":true,
"curiosity":true,
"platform":"",
"content_style":"",
"brand_position":"",
"offer_position":"",
"funnel":"",
"viral":"High",
"priority":[]
}

Never explain.

Never use markdown.

Return JSON only.
"""


def think(product, topic):

    prompt = f"""
{SYSTEM_PROMPT}

PRODUCT:

{product}

TOPIC:

{topic}

Think like the executive board before any other AI department starts working.
"""


    result = ask_ai(prompt)


    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()


    try:

        return json.loads(result)


    except Exception as e:


        print("=" * 60)
        print("Thinking Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(result)


        return {


            "customer":
            "Digital creators, freelancers, marketers and business owners",


            "awareness":
            "Problem Aware",


            "pain":
            "Creating content is slow and overwhelming",


            "desire":
            "Grow faster using AI",


            "dream":
            "Build an automated online business",


            "objection":
            "AI looks too complicated",


            "emotion":
            "Curiosity + Urgency",


            "goal":
            "Educate first, convert second",


            "marketing_angle":
            "Problem → Solution → Transformation",


            "sales_angle":
            "Value before selling",


            "hook":
            "Contrarian + Curiosity",


            "cta":
            "Final 20% of the video",


            "urgency":
            True,


            "curiosity":
            True,


            "platform":
            "YouTube Shorts, TikTok, Facebook Reels",


            "content_style":
            "Fast paced cinematic",


            "brand_position":
            "Premium AI Education",


            "offer_position":
            "Ultimate AI Toolkit",


            "funnel":
            "Lead Generation",


            "viral":
            "High",


            "priority":

            [

                "marketing",

                "psychology",

                "offer",

                "director",

                "storyboard",

                "prompt",

                "script",

                "voice"

            ]

        }
