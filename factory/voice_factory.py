from brain.voice_engine import generate_voice


class VoiceFactory:

    def __init__(self):

        print("Voice Factory Ready")


    def create(self, script):

        print("Generating AI Voice...")

        voice_file = generate_voice(
            script
        )

        return {

            "script": script,

            "voice_file": voice_file

        }


voice_factory = VoiceFactory()
