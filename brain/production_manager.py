from brain.pipeline import pipeline
from brain.seo_engine import generate_seo
from brain.memory_engine import memory


class ProductionManager:

    def __init__(self):

        print("Production Manager Ready")


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)


        print("Running AI Brain...")

        project = pipeline.execute(
            topic
        )


        print("Generating SEO...")

        seo = generate_seo(
            topic
        )


        project["seo"] = seo


        print("Preparing Production Package...")


        production = {

            "topic": topic,

            "status": "READY",

            "project": project

        }


        print("Saving Final Production Memory...")


        memory.save(
            topic,
            production
        )


        print("Production Package Ready")


        return production



production = ProductionManager()
