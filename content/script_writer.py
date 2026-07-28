from brain.ai import ask_ai
from config import BRAND_NAME


def generate_script(topic):

    prompt = f"""
You are a professional TikTok script writer.

Write one viral 30-second TikTok script.

Topic:
{topic}

Requirements:
- Strong hook in the first sentence
- Educational
- Exciting
- Easy English
- Mention {BRAND_NAME} naturally if appropriate
- End with a strong call to action
- Do NOT use emojis
"""

    return ask_ai(prompt)
