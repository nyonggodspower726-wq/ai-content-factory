from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub SEO AI.

Your job is to optimize every video for search.

Return JSON only.

Create:

1. SEO Title
2. Clickable Title
3. Description
4. Keywords
5. Tags
6. Hashtags
7. Search Intent
8. Thumbnail Text

Example:

{
"title":"",
"click_title":"",
"description":"",
"keywords":[
"",
""
],
"tags":[
"",
""
],
"hashtags":[
"",
""
],
"intent":"",
"thumbnail":""
}
"""


def generate_seo(topic):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":f"Generate SEO for {topic}"
            }

        ],

        temperature=0.7,

        max_tokens=1200

    )

    return response.choices[0].message.content
