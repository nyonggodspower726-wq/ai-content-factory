from brain.pipeline import pipeline


class ProductionManager:

    def __init__(self):

        print("Production Manager Ready")


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO")
        print("=" * 60)

        project = pipeline.execute(topic)

        print("Production Plan Completed")

        production = {

            "topic": topic,

            "status": "READY",

            "project": project

        }

        return production


production = ProductionManager()
