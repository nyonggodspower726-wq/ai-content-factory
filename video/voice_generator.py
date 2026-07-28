import os
import asyncio
import edge_tts


VOICE = "en-US-GuyNeural"


async def create_voice(text, output_file):

    communicate = edge_tts.Communicate(
        text,
        VOICE
    )

    await communicate.save(output_file)



def generate_voice(script):

    print("Generating professional AI voice...")

    os.makedirs("output", exist_ok=True)

    voice_file = "output/voice.mp3"

    try:
        asyncio.run(
            create_voice(
                script,
                voice_file
            )
        )

        print("AI voice generated successfully.")

        return voice_file

    except Exception as e:
        print(f"Voice generation failed: {e}")
        return None
