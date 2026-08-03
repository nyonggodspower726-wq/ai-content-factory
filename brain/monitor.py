import time


class AIMonitor:

    def __init__(self):

        self.steps = []

        self.session_start = None

        self.total_errors = 0


    def start(self, engine):

        if self.session_start is None:

            self.session_start = time.time()

        self.steps.append({

            "engine": engine,

            "start": time.time(),

            "provider": "-",

            "status": "RUNNING"

        })

        print("=" * 60)

        print(f"STARTING {engine.upper()}")

        print("=" * 60)


    def finish(self, provider="-"):

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

        step["error"] = str(error)

        self.total_errors += 1

        print(f"{step['engine']} failed")

        print(error)


    def summary(self):

        total_runtime = round(

            time.time() - self.session_start,

            2

        ) if self.session_start else 0

        print()

        print("=" * 60)

        print("PROMPTPROHUB AI STUDIO REPORT")

        print("=" * 60)

        for step in self.steps:

            duration = step.get("duration", "-")

            provider = step.get("provider", "-")

            status = step.get("status", "-")

            print(

                f"{step['engine']} | {provider} | {status} | {duration}s"

            )

        print("=" * 60)

        print(f"Total Runtime : {total_runtime}s")

        print(f"Total Engines : {len(self.steps)}")

        print(f"Total Errors  : {self.total_errors}")

        print("=" * 60)


    def reset(self):

        self.steps = []

        self.session_start = None

        self.total_errors = 0


monitor = AIMonitor()
