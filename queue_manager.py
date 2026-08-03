class QueueManager:

    def __init__(self):
        self.jobs = []

    def add(self, topic):
        self.jobs.append(topic)
        print(f"Added to queue: {topic}")

    def complete(self, topic):
        if topic in self.jobs:
            self.jobs.remove(topic)
        print(f"Completed: {topic}")

    def pending(self):
        return self.jobs


queue_manager = QueueManager()
