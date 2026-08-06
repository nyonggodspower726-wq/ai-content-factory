from brain.ai_router import ask_ai


SYSTEM_PROMPT = """
You are PromptProHub Emotion Voice Director.

Your job is to improve narration quality for AI voice.

You DO NOT add voice instructions.

You DO NOT write:

[pause]

[emphasis]

(pause)

(emphasis)

whisper

slow down

speed up

dramatic pause


The output must be ONLY the final narration text that a human voice should speak.

Use natural writing techniques:

- Short sentences for impact.
- Natural rhythm.
- Curiosity.
- Emotion.
- Strong storytelling.
- Smooth transitions.

Do not explain your changes.

Do not add stage directions.

Return ONLY clean narration text suitable for Edge-TTS.
"""


def build_emotional_script(script, voice_profile):


    prompt = f"""

{SYSTEM_PROMPT}


Voice Style:

{voice_profile}


Original Script:

{script}

"""


    response = ask_ai(
        prompt
    )


    return response.strip()
