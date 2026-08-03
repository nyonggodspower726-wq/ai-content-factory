from production_controller import controller
from monitor import monitor
from brain.credit_manager import credits


class Pipeline:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO PIPELINE")
        print("=" * 60)

    def run(self, topic):

        monitor.start()

        monitor.update(
            "Pipeline",
            "STARTED"
        )

        try:

            credits.use_groq()

            project = controller.produce(
                topic
            )

            monitor.update(
                "Production",
                "SUCCESS"
            )

            monitor.report()

            return project

        except Exception as e:

            monitor.update(
                "Production",
                "FAILED"
            )

            print(e)

            monitor.report()

            return None


pipeline = Pipeline()
