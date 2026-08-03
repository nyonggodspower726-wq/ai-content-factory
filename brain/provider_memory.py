class ProviderMemory:

    def __init__(self):

        self.current_provider = None

    def get(self):

        return self.current_provider

    def set(self, provider):

        self.current_provider = provider

    def clear(self):

        self.current_provider = None


provider_memory = ProviderMemory()
