from collections import deque


class QueueManager:

    def __init__(self):

        self.queue = deque()

        self.completed = []

    def add(self, topic):

        self.queue.append(topic)

        print(f"Added to queue: {topic}")

    def next(self):

        if len(self.queue) == 0:
            return None

        return self.queue.popleft()

    def complete(self, topic):

        self.completed.append(topic)

    def pending(self):

        return list(self.queue)

    def history(self):

        return self.completed

    def size(self):

        return len(self.queue)

    def clear(self):

        self.queue.clear()

        self.completed.clear()


queue_manager = QueueManager()
