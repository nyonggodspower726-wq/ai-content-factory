from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_voice(script):

    print("Generating AI voice...")

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=script,
    )

    with open("output.mp3", "wb") as f:
        f.write(response.read())

    return "output.mp3"
