from collections import deque
from datetime import datetime


class QueueManager:

    def __init__(self):

        self.queue = deque()

        self.completed = []

        self.failed = []


    def add(self, topic):

        job = {

            "topic": topic,

            "created": datetime.now().isoformat(),

            "status": "PENDING"

        }

        self.queue.append(job)

        print(f"Added to queue: {topic}")


    def next(self):

        if not self.queue:

            return None

        job = self.queue.popleft()

        job["status"] = "RUNNING"

        return job


    def complete(self, topic):

        self.completed.append({

            "topic": topic,

            "completed": datetime.now().isoformat(),

            "status": "COMPLETED"

        })


    def fail(self, topic, error):

        self.failed.append({

            "topic": topic,

            "error": str(error),

            "time": datetime.now().isoformat(),

            "status": "FAILED"

        })


    def pending(self):

        return list(self.queue)


    def history(self):

        return self.completed


    def failed_jobs(self):

        return self.failed


    def size(self):

        return len(self.queue)


    def report(self):

        print("=" * 60)
        print("QUEUE REPORT")
        print("=" * 60)

        print(f"Pending Jobs   : {len(self.queue)}")
        print(f"Completed Jobs : {len(self.completed)}")
        print(f"Failed Jobs    : {len(self.failed)}")

        print("=" * 60)


    def clear(self):

        self.queue.clear()

        self.completed.clear()

        self.failed.clear()


queue_manager = QueueManager()
