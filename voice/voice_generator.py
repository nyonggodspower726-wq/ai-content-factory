import os
import asyncio
import edge_tts

from voice.emotion_engine import build_emotional_script


VOICE_MAP = {

    "male": "en-US-BrianMultilingualNeural",

    "female": "en-US-AvaMultilingualNeural",

    "professional": "en-US-BrianMultilingualNeural",

    "motivational": "en-US-AndrewMultilingualNeural",

    "friendly": "en-US-EricNeural"

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


    # FIX DICTIONARY ERROR
    if isinstance(voice_profile, dict):

        gender = voice_profile.get(
            "gender",
            "male"
        )

        if gender.lower() == "female":
            voice_profile = "female"

        else:
            voice_profile = "male"



    voice_profile = str(
        voice_profile
    ).lower()



    voice = VOICE_MAP.get(

        voice_profile,

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



        if not os.path.exists(
            voice_file
        ):

            raise Exception(
                "Voice file missing"
            )



        print(
            "VOICE CREATED:",
            voice
        )


        return voice_file



    except Exception as e:


        print(
            "VOICE ENGINE FAILED:",
            e
        )


        return None
