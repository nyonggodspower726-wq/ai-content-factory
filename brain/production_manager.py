from brain.pipeline import pipeline
from brain.script_engine import generate_script
from brain.voice_engine import generate_voice


class ProductionManager:

    def __init__(self):
        print("PromptProHub AI Studio Brain Online")


    def produce(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)

        print("AI Brain generating campaign...")

        project = pipeline.execute()


        print("Generating Script...")

        script = generate_script(project)


        print("Generating Voice Profile...")

        voice = generate_voice(project)


        production = {

            "topic": project.get("topic"),

            "project": project,

            "script": script,

            "voice": voice,

            "status": "READY FOR VIDEO"

        }


        return production


production = ProductionManager()
