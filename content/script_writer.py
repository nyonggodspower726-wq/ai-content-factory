from ai import ask_ai
from config import BRAND_NAME


def generate_script(topic):

    prompt = f"""
You are a world-class viral short-form copywriter.

Write ONE 30-45 second TikTok, YouTube Shorts, Instagram Reels and Facebook Reels script.

Topic:
{topic}

Requirements:

- Start with a shocking hook in the first sentence.
- Explain a common problem people face.
- Give one practical solution.
- Create curiosity so viewers want more.
- Use very simple English.
- Sound natural and conversational.
- Mention {BRAND_NAME} naturally if appropriate.

- End with this exact call to action:

Click the link in my bio to download premium AI prompt templates that save you hours of work.

Rules:

- No emojis.
- No hashtags.
- No stage directions.
- No titles.
- Output ONLY the spoken script.
"""

    return ask_ai(prompt)
