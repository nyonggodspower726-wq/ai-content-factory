from brain.pipeline import pipeline

from brain.script_engine import generate_script
from brain.voice_engine import generate_voice


class ProductionManager:

    def __init__(self):

        print("PromptProHub AI Studio Brain Online")


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)


        print(f"Campaign Topic: {topic}")


        project = pipeline.execute(topic)


        print("Generating Script...")

        script = generate_script(project)


        print("Generating Voice Profile...")

        voice = generate_voice(project)


        production = {

            "topic": topic,

            "project": project,

            "script": script,

            "voice": voice,

            "status": "READY FOR VIDEO"

        }


        return production



production = ProductionManager()
