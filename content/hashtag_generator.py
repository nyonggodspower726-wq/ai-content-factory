from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def generate_hashtags():

    prompt = """
Generate 15 trending TikTok hashtags for AI, business,
digital products, freelancing and online income.

Return only hashtags.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
