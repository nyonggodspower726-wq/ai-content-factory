from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """

You are PromptProHub AI Voice Director.

Your job is ONLY to create voice settings.

You DO NOT write narration.
You DO NOT create spoken sentences.
You DO NOT put instructions inside the script.

Return JSON only.

The narration text must stay separate from voice directions.

Never output:

[pause]

[emphasis]

(pause)

(emphasis)

"say slowly"

"say loudly"


Create:

1. Voice Gender
2. Voice Age
3. Voice Personality
4. Voice Emotion
5. Emotion Curve
6. Speaking Speed
7. Speaking Rhythm
8. Pause Locations
9. Emphasis Words
10. CTA Style
11. Pronunciation Dictionary


Example:

{
"gender":"Male",

"age":"Young Adult",

"personality":"Confident AI Expert",

"emotion":"Curious",

"emotion_curve":[
"Curiosity",
"Excitement",
"Trust",
"Urgency"
],

"speed":{
"hook":"Fast",
"body":"Medium",
"cta":"Slow"
},

"rhythm":"Natural",

"pause_locations":[
"After the first sentence",
"Before the reveal",
"Before CTA"
],

"emphasis_words":[
"AI prompts",
"automation",
"save time",
"business"
],

"cta_style":
"Friendly persuasive",

"pronunciation":{

"PromptProHub":
"Prompt Pro Hub",

"ChatGPT":
"Chat G P T",

"OpenAI":
"Open A I",

"AI":
"A I",

"CRT":
"C R T"

}

}

"""


def generate_voice(project):


    prompt = f"""

{SYSTEM_PROMPT}


Project:

{project}

"""


    try:

        response = ask_ai(
            prompt
        )


        response = (
            response
            .replace("```json","")
            .replace("```","")
            .strip()
        )


        return json.loads(
            response
        )


    except Exception as e:


        print(
            "Voice Director Error:",
            e
        )


        return {

            "gender":"Male",

            "age":"Young Adult",

            "personality":
            "Confident Mentor",

            "emotion":
            "Curious",

            "speed":{
                "hook":"Fast",
                "body":"Medium",
                "cta":"Slow"
            },

            "pronunciation":{

                "PromptProHub":
                "Prompt Pro Hub",

                "ChatGPT":
                "Chat G P T",

                "OpenAI":
                "Open A I",

                "AI":
                "A I",

                "CRT":
                "C R T"

            }

        }
