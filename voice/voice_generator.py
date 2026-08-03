import os
import asyncio
import edge_tts

from voice.emotion_engine import build_emotional_script


VOICE = "en-US-BrianMultilingualNeural"


async def create_voice(text, output_file):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save(output_file)



def generate_voice(script, voice_profile="professional"):

    print("=" * 60)
    print("AI VOICE DIRECTOR")
    print("=" * 60)


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
                voice_file
            )
        )


        print("Professional AI Voice Created")


        return voice_file


    except Exception as e:

        print("VOICE ERROR")

        print(str(e))

        return None
