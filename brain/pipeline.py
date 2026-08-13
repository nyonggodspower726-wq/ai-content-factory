from production_controller import controller
from brain.monitor import monitor
from brain.credit_manager import credits

class Pipeline:
    def __init__(self):
        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO PIPELINE ONLINE")
        print("=" * 60)

    def run(self, topic, platform="tiktok", video_number=1):
        monitor.reset()
        monitor.start("Pipeline")

        try:
            print("=" * 60)
            print("PIPELINE START")
            print("=" * 60)
            print(f"Topic: {topic}")
            print(f"Platform: {platform.upper()}")
            print(f"Video: {video_number}/4")
            print("=" * 60)

            print("Checking AI credits...")
            credits.use_groq()

            print("Starting Production Controller...")

            # ProductionController currently accepts topic only.
            # Keep the new platform/video metadata at the Pipeline level
            # without breaking the existing controller interface.
            project = controller.produce(topic)

            if not project:
                print("Controller returned no project.")
                monitor.fail("No production project created")
                monitor.summary()
                return None

            if isinstance(project, dict):
                project["platform"] = platform
                project["video_number"] = video_number

            monitor.finish("Groq")
            monitor.finish("Production")
            monitor.summary()

            print("=" * 60)
            print("PIPELINE COMPLETE")
            print("=" * 60)
            print(f"Platform: {platform.upper()}")
            print(f"Video: {video_number}/4")
            print("=" * 60)

            return project

        except Exception as e:
            print("=" * 60)
            print("PIPELINE FAILED")
            print("=" * 60)
            print(f"Error Type: {type(e).__name__}")
            print(f"Error: {e}")
            print("=" * 60)

            monitor.fail(e)
            monitor.summary()

            return None

pipeline = Pipeline()
