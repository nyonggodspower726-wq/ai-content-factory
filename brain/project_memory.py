class ProjectMemory:

    def __init__(self):

        self.data = {}

    def set(self, key, value):

        self.data[key] = value

    def get(self, key, default=None):

        return self.data.get(key, default)

    def all(self):

        return self.data

    def clear(self):

        self.data = {}


project = ProjectMemory()
