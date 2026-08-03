from brain.queue_manager import queue_manager
from dashboard.dashboard import dashboard
from scheduler import run_bot


class ControlCenter:

    def __init__(self):

        self.running = False

    def start(self):

        self.running = True

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO STARTED")
        print("=" * 60)

    def stop(self):

        self.running = False

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO STOPPED")
        print("=" * 60)

    def add_topic(self, topic):

        queue_manager.add(topic)

    def process_next(self):

        if not self.running:

            print("Factory is stopped.")
            return

        topic = queue_manager.next()

        if topic is None:

            print("Queue is empty.")
            return

        print(f"Processing: {topic}")

        run_bot()

        queue_manager.complete(topic)

    def show_dashboard(self):

        dashboard.show()

    def queue_status(self):

        print("=" * 60)
        print("QUEUE STATUS")
        print("=" * 60)

        print(f"Pending : {queue_manager.size()}")

        for topic in queue_manager.pending():

            print(f"- {topic}")

        print()

        print("Completed:")

        for topic in queue_manager.history():

            print(f"✓ {topic}")


control = ControlCenter()
