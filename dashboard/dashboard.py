import os
from datetime import datetime
from zoneinfo import ZoneInfo

from brain.queue_manager import queue_manager
from brain.provider_memory import provider_memory
from brain.project_memory import project
from brain.monitor import monitor


class Dashboard:

    def __init__(self):

        self.version = "PromptProHub AI Studio v2.0"

    def clear(self):

        os.system("cls" if os.name == "nt" else "clear")

    def show(self):

        self.clear()

        print("=" * 70)
        print(self.version)
        print("=" * 70)

        print(
            f"Time: {datetime.now(ZoneInfo('Africa/Lagos')).strftime('%Y-%m-%d %H:%M:%S')}"
        )

        print()

        print(f"Current AI Provider : {provider_memory.get()}")

        print(f"Videos Waiting      : {queue_manager.size()}")

        print(f"Completed Videos    : {len(queue_manager.history())}")

        print()

        print("=" * 70)
        print("QUEUE")
        print("=" * 70)

        pending = queue_manager.pending()

        if pending:

            for i, topic in enumerate(pending, start=1):

                print(f"{i}. {topic}")

        else:

            print("Queue Empty")

        print()

        print("=" * 70)
        print("CURRENT PROJECT")
        print("=" * 70)

        for key, value in project.export().items():

            print(f"{key}: {value}")

        print()

        print("=" * 70)
        print("ENGINE REPORT")
        print("=" * 70)

        for step in monitor.steps:

            duration = step.get("duration", "-")

            provider = step.get("provider", "-")

            status = step.get("status", "-")

            print(
                f"{step['engine']} | {provider} | {status} | {duration}s"
            )

        print("=" * 70)


dashboard = Dashboard()
