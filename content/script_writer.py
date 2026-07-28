from groq import Groq
from config import GROQ_API_KEY, BRAND_NAME

client = Groq(api_key=GROQ_API_KEY)

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

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content
