from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_caption(topic):

    prompt = f"""
Write one engaging TikTok caption for:

{topic}

Requirements:
- Short
- Catchy
- Encourage engagement
- No emojis
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
