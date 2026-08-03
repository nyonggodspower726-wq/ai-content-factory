from production_controller import controller
from brain.monitor import monitor
from brain.credit_manager import credits


class Pipeline:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO PIPELINE")
        print("=" * 60)

    def run(self, topic):

        monitor.reset()

        monitor.start("Pipeline")

        try:

            credits.use_groq()

            project = controller.produce(topic)

            monitor.finish("Groq")

            monitor.summary()

            return project

        except Exception as e:

            monitor.fail(e)

            print(e)

            monitor.summary()

            return None


pipeline = Pipeline()
