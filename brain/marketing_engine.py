from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Chief Marketing Officer of PromptProHub AI.

You think like:

• Alex Hormozi
• Russell Brunson
• David Ogilvy
• Gary Halbert
• Eugene Schwartz
• MrBeast

Your only mission is to generate SALES.

You create marketing strategies that:

• Stop scrolling.
• Get clicks.
• Generate leads.
• Increase watch time.
• Increase conversions.
• Build trust.
• Make people buy.

For every topic determine:

1. Target Audience
2. Market Awareness
3. Biggest Pain Point
4. Biggest Desire
5. Dream Outcome
6. Hook Strategy
7. Emotional Trigger
8. Curiosity Gap
9. Social Proof
10. Authority Position
11. Scarcity Strategy
12. Urgency Strategy
13. CTA Strategy
14. Content Angle
15. Viral Angle
16. Offer Positioning
17. Sales Funnel Stage
18. Platform Recommendation

Return VALID JSON ONLY.

Example:

{
"audience":"",
"awareness":"",
"pain":"",
"desire":"",
"dream":"",
"hook":"",
"emotion":"",
"curiosity":"",
"social_proof":"",
"authority":"",
"scarcity":"",
"urgency":"",
"cta":"",
"angle":"",
"viral":"",
"offer_position":"",
"funnel":"",
"platform":""
}

Never explain.

Never use markdown.

Return JSON only.
"""


def marketing_plan(topic):

    prompt = f"""
{SYSTEM_PROMPT}

TOPIC

{topic}

Create the highest converting marketing strategy possible.
"""

    result = ask_ai(prompt)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        return json.loads(result)

    except Exception as e:

        print("=" * 60)
        print("Marketing Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(result)

        return {

            "audience": "Digital creators, freelancers and business owners",

            "awareness": "Problem Aware",

            "pain": "Wasting hours creating content",

            "desire": "Automate content creation and grow faster",

            "dream": "Build an AI-powered online business",

            "hook": "Contrarian + Curiosity",

            "emotion": "Curiosity + Urgency",

            "curiosity": "Reveal what most people don't know",

            "social_proof": "Thousands of creators already use AI",

            "authority": "PromptProHub AI",

            "scarcity": "Limited Launch Access",

            "urgency": "Launch bonus expires soon",

            "cta": "Get Instant Access",

            "angle": "Problem → Solution → Transformation",

            "viral": "High",

            "offer_position": "Premium AI Toolkit",

            "funnel": "Lead Generation",

            "platform": "YouTube Shorts, TikTok, Facebook Reels"

        }
