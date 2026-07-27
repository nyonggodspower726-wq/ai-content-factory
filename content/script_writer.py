from openai import OpenAI
from config import OPENAI_API_KEY, BRAND_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic):

    prompt = f"""
You are a professional TikTok script writer.

Write one viral 30-second TikTok script.

Topic:
{topic}

Requirements:
- Strong hook in first sentence
- Educational
- Exciting
- Easy English
- Mention the website naturally
- End with a strong call to action
- Do NOT use emojis
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
