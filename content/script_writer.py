import google.generativeai as genai
from config import GEMINI_API_KEY, BRAND_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

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

    response = model.generate_content(prompt)

    return response.text
