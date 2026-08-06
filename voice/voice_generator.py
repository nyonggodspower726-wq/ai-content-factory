import os
import asyncio
import edge_tts

from voice.emotion_engine import build_emotional_script


VOICE_MAP = {

    "professional": "en-US-BrianMultilingualNeural",

    "confident": "en-US-BrianMultilingualNeural",

    "motivational": "en-US-AndrewMultilingualNeural",

    "friendly": "en-US-EricNeural",

    "female": "en-US-AvaMultilingualNeural",

    "luxury": "en-US-BrianMultilingualNeural"

}


async def create_voice(text, output_file, voice):

    communicate = edge_tts.Communicate(

        text=text,

        voice=voice

    )

    await communicate.save(output_file)


def generate_voice(

    script,

    voice_profile="professional"

):

    print("=" * 60)
    print("PROMPTPROHUB AI VOICE DIRECTOR")
    print("=" * 60)

    voice = VOICE_MAP.get(

        voice_profile.lower(),

        VOICE_MAP["professional"]

    )

    emotional_script = build_emotional_script(

        script,

        voice_profile

    )

    os.makedirs(

        "output",

        exist_ok=True

    )

    voice_file = "output/voice.mp3"

    try:

        asyncio.run(

            create_voice(

                emotional_script,

                voice_file,

                voice

            )

        )

        # -----------------------------------------
        # Verify voice file exists
        # -----------------------------------------

        if not os.path.exists(voice_file):

            raise Exception(

                "Voice file was not created."

            )

        if os.path.getsize(voice_file) == 0:

            raise Exception(

                "Voice file is empty."

            )

        print("=" * 60)
        print("PROFESSIONAL AI VOICE CREATED")
        print("=" * 60)
        print("Voice :", voice)
        print("File  :", voice_file)
        print(
            f"Size  : {os.path.getsize(voice_file)} bytes"
        )

        return voice_file

    except Exception as e:

        print("=" * 60)
        print("VOICE ENGINE FAILED")
        print("=" * 60)
        print(e)

        return None
