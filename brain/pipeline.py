from production_controller import controller

from brain.monitor import monitor
from brain.credit_manager import credits


class Pipeline:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO PIPELINE ONLINE")
        print("=" * 60)

    def run(self, topic):

        monitor.reset()

        monitor.start(
            "Pipeline"
        )

        try:

            print(
                "Checking AI credits..."
            )

            credits.use_groq()

            print(
                "Starting Production Controller..."
            )

            project = controller.produce(
                topic
            )

            if not project:

                print(
                    "Controller returned no project."
                )

                monitor.fail(
                    "No production project created"
                )

                monitor.summary()

                return None

            monitor.finish(
                "Groq"
            )

            monitor.finish(
                "Production"
            )

            monitor.summary()

            return project

        except Exception as e:

            print("=" * 60)
            print("PIPELINE FAILED")
            print("=" * 60)

            print(
                "ERROR TYPE:",
                type(e).__name__
            )

            print(
                "ERROR:",
                str(e)
            )

            print("=" * 60)

            monitor.fail(
                e
            )

            monitor.summary()

            return None


pipeline = Pipeline()
