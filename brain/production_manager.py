from brain.pipeline import pipeline
from brain.script_engine import generate_script
from brain.voice_engine import generate_voice
from video.generator import create_video


class ProductionManager:

    def __init__(self):

        print("Production Manager Ready")


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)

        project = pipeline.execute(topic)

        print("Generating Script...")

        script = generate_script(project)

        print("Generating Voice Profile...")

        voice = generate_voice(project)

        print("Preparing Video Production...")

        production = {

            "topic": topic,

            "project": project,

            "script": script,

            "voice": voice,

            "status": "READY FOR VIDEO"

        }

        return production


production = ProductionManager()
