from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
You are PromptProHub Debate Engine.

You are moderating a meeting between AI departments.

Departments:
- Audience AI
- Marketing AI
- Psychology AI
- Director AI
- Storyboard AI
- Viral AI
- SEO AI

Their goal is ONE thing:

Create the highest converting advertisement.

Do NOT simply agree.

Challenge weak ideas.

Improve weak hooks.

Improve weak CTA.

Improve weak emotions.

Debate until the campaign is excellent.

Return JSON only.

{
 "audience_feedback":"",
 "marketing_feedback":"",
 "psychology_feedback":"",
 "director_feedback":"",
 "storyboard_feedback":"",
 "viral_feedback":"",
 "seo_feedback":"",
 "final_strategy":""
}
"""

def debate(project):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },

            {
                "role":"user",
                "content":str(project)
            }

        ],

        temperature=0.9,

        max_tokens=1800

    )

    return response.choices[0].message.content
