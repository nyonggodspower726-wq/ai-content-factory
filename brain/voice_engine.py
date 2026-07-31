from groq import Groq
from config import GROQ_API_KEY

client = Groq(
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are PromptProHub Voice AI.

Your job is to choose the perfect narration style.

Return JSON only.

Determine:

1. Voice Gender
2. Voice Age
3. Voice Emotion
4. Voice Speed
5. Voice Tone
6. Voice Style
7. Pause Positions
8. Emphasis Words

Example:

{
"gender":"Male",
"age":"Young Adult",
"emotion":"Confident",
"speed":"Medium",
"tone":"Professional",
"style":"Commercial",
"pauses":[
"After Hook",
"Before CTA"
],
"emphasis":[
"FREE",
"LIMITED",
"TODAY"
]
}
"""


def generate_voice(project):

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

        temperature=0.7,

        max_tokens=1000

    )

    return response.choices[0].message.content
