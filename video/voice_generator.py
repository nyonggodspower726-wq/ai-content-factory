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


def generate_voice(script, voice_profile):

    print("=" * 60)
    print("AI VOICE DIRECTOR")
    print("=" * 60)

    print("Applying emotions...")

    emotional_script = build_emotional_script(
        script,
        voice_profile
    )

    os.makedirs("output", exist_ok=True)

    voice_file = "output/voice.mp3"

    try:

        try:

            asyncio.run(
                create_voice(
                    emotional_script,
                    voice_file
                )
            )

        except RuntimeError:

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(
                create_voice(
                    emotional_script,
                    voice_file
                )
            )

            loop.close()

        print("Professional AI Voice Created")

        return voice_file

    except Exception as e:

        print(f"Voice generation failed: {e}")

        return None
