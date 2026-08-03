from brain.pipeline import pipeline

from brain.script_engine import generate_script
from brain.voice_engine import generate_voice as create_voice_profile

from video.voice_generator import generate_voice as create_audio


class ProductionManager:

    def __init__(self):

        print("PromptProHub AI Studio Brain Online")


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)

        print(f"Campaign Topic: {topic}")


        project = pipeline.run(topic)


        print("Generating Script...")

        script = generate_script(project)


        print("Generating Voice Profile...")

        voice_profile = create_voice_profile(project)


        print("Generating Emotional AI Voice...")

        voice_file = create_audio(
            script,
            voice_profile
        )


        production = {

            "topic": topic,

            "project": project,

            "script": script,

            "voice_profile": voice_profile,

            "voice": voice_file,

            "status": "READY FOR VIDEO"

        }


        return production



production = ProductionManager()
