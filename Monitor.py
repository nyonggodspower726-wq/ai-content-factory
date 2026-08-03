import time
from datetime import datetime


class ProductionMonitor:

    def __init__(self):

        self.status = {}

        self.start_time = None

    def start(self):

        self.start_time = time.time()

        print("=" * 60)
        print("PRODUCTION MONITOR STARTED")
        print("=" * 60)

    def update(self, engine, state):

        self.status[engine] = {

            "status": state,

            "time": datetime.now().strftime("%H:%M:%S")

        }

        print(f"[{engine}] -> {state}")

    def report(self):

        print("=" * 60)
        print("PRODUCTION REPORT")
        print("=" * 60)

        for engine, data in self.status.items():

            print(

                f"{engine:<25}"

                f"{data['status']:<12}"

                f"{data['time']}"

            )

        if self.start_time:

            duration = round(

                time.time() - self.start_time,

                2

            )

            print("-" * 60)

            print(f"Total Runtime: {duration} seconds")

        print("=" * 60)

    def clear(self):

        self.status = {}

        self.start_time = None


monitor = ProductionMonitor()
