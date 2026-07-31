from brain.pipeline import pipeline
from brain.production_manager import production


class PromptProHubAI:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)

    def create(self, topic):

        print(f"Creating project for: {topic}")

        project = pipeline.execute(topic)

        result = production.produce(topic)

        return {

            "project": project,

            "production": result

        }


studio = PromptProHubAI()
