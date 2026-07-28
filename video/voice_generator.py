import os
from gtts import gTTS


def generate_voice(script):

    print("Generating AI voice...")

    os.makedirs("output", exist_ok=True)

    voice_file = "output/voice.mp3"

    try:
        tts = gTTS(
            text=script,
            lang="en",
            slow=False
        )

        tts.save(voice_file)

        print("Voice generated successfully.")

        return voice_file

    except Exception as e:
        print(f"Voice generation failed: {e}")
        return None
