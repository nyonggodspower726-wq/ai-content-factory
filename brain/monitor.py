import time


class AIMonitor:

    def __init__(self):

        self.steps = []

    def start(self, engine):

        self.steps.append({
            "engine": engine,
            "start": time.time(),
            "provider": "",
            "status": "RUNNING"
        })

        print("=" * 60)
        print(f"STARTING {engine.upper()}")
        print("=" * 60)

    def finish(self, provider=""):

        step = self.steps[-1]

        step["provider"] = provider
        step["status"] = "SUCCESS"

        duration = round(
            time.time() - step["start"],
            2
        )

        step["duration"] = duration

        print(
            f"{step['engine']} completed in {duration}s"
        )

    def fail(self, error):

        step = self.steps[-1]

        step["status"] = "FAILED"

        print(
            f"{step['engine']} failed"
        )

        print(error)

    def summary(self):

        print("\n")
        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO REPORT")
        print("=" * 60)

        for step in self.steps:

            duration = step.get("duration", "-")

            provider = step.get("provider", "-")

            print(
                f"{step['engine']} | {provider} | {step['status']} | {duration}s"
            )

        print("=" * 60)


monitor = AIMonitor()
