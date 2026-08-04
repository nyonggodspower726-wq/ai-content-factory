from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Founder, CEO and Chief Growth Officer of PromptProHub AI.

You think like:

• Alex Hormozi
• Russell Brunson
• Steve Jobs
• David Ogilvy
• Gary Halbert
• Claude Hopkins
• MrBeast
• Sam Altman

You NEVER create average content.

Your mission is to create campaigns that:

• Stop scrolling.
• Capture attention instantly.
• Build trust.
• Create desire.
• Trigger emotion.
• Generate clicks.
• Generate leads.
• Generate sales.

Before making any decision you silently analyse:

1. Audience sophistication.
2. Market awareness.
3. Biggest customer pain.
4. Biggest customer dream.
5. Emotional trigger.
6. Buying objections.
7. Viral potential.
8. Sales potential.
9. Best platform.
10. Best content angle.

Then decide:

- Business objective
- Target customer
- Campaign type
- Customer awareness stage
- Emotional direction
- Marketing framework
- Offer priority
- Funnel stage
- Recommended platform
- Video style
- Hook style
- CTA style
- Expected outcome
- Which departments should receive priority

Return VALID JSON ONLY.

Example:

{
    "objective":"",
    "customer":"",
    "campaign":"",
    "awareness":"",
    "emotion":"",
    "marketing":"",
    "priority":"",
    "platform":"",
    "video_style":"",
    "hook_style":"",
    "cta_style":"",
    "goal":"",
    "departments":[]
}

Never return markdown.

Never explain.

Never return ```.

Always think like a billion-dollar marketing company.
"""


class CEOEngine:

    def __call__(self, topic, product="PromptProHub Products"):

        return self.review(topic, product)


    def review(self, topic, product="PromptProHub Products"):

        prompt = f"""
{SYSTEM_PROMPT}

TOPIC

{topic}

PRODUCT

{product}

Make the highest-converting business decision possible.
"""

        raw = ask_ai(prompt)

        raw = raw.replace("```json", "")
        raw = raw.replace("```", "")
        raw = raw.strip()

        try:

            return json.loads(raw)

        except Exception as e:

            print("=" * 60)
            print("CEO Engine JSON parsing failed")
            print(e)
            print("=" * 60)

            print(raw)

            return {

                "objective": "Generate qualified leads",

                "customer": "Digital creators, freelancers, marketers and business owners",

                "campaign": "Direct Response Marketing",

                "awareness": "Problem Aware",

                "emotion": "Curiosity + Urgency",

                "marketing": "PAS + AIDA",

                "priority": "Lead Generation",

                "platform": "YouTube Shorts, TikTok, Facebook Reels",

                "video_style": "Fast paced cinematic",

                "hook_style": "Scroll stopping",

                "cta_style": "Urgent",

                "goal": "Traffic → Leads → Sales",

                "departments": [

                    "thinking",

                    "marketing",

                    "psychology",

                    "director",

                    "storyboard",

                    "prompt",

                    "script",

                    "voice",

                    "video",

                    "seo"

                ]

            }


ceo = CEOEngine()
