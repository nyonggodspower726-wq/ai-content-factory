from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the CEO of PromptProHub AI.

You are NOT a script writer.
You are NOT a marketer.
You are the executive decision maker.

Your responsibilities:

1. Understand the user's request.
2. Choose the business objective.
3. Choose the best customer.
4. Choose the campaign type.
5. Choose the emotional direction.
6. Choose the marketing direction.
7. Decide if education or selling comes first.
8. Decide the expected outcome.
9. Instruct every AI department.

Return JSON only.
"""


class CEOEngine:

    def __call__(self, topic, product="PromptProHub Products"):
        """
        Allows:
            ceo(topic)
        instead of:
            ceo.review(topic)
        """
        return self.review(topic, product)

    def review(self, topic, product="PromptProHub Products"):

        prompt = f"""
{SYSTEM_PROMPT}

Topic:
{topic}

Product:
{product}
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

            return {
                "objective": "Create High Quality AI Content",
                "customer": "Digital Creators",
                "campaign": "Educational",
                "emotion": "Curiosity",
                "marketing": "Problem Solution",
                "priority": "Value First",
                "goal": "Conversions",
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
