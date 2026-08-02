from brain.ai_router import ask_ai


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

    prompt = f"""
{SYSTEM_PROMPT}

Generate SEO for:

{topic}
"""

    return ask_ai(prompt)
