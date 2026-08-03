from brain.monitor import monitor
from brain.recovery_manager import recovery
from brain.queue_manager import queue_manager
from brain.provider_memory import provider_memory


class MasterEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB MASTER ENGINE ONLINE")
        print("=" * 60)


    def initialize(self, topic):

        print("=" * 60)
        print("MASTER ENGINE INITIALIZING")
        print("=" * 60)

        queue_manager.add(topic)

        monitor.reset()

        recovery.reset()

        print("Factory Ready.")


    def before_ai(self, provider):

        provider_memory.remember(provider)

        monitor.start(f"AI Provider : {provider}")


    def after_ai(self, provider):

        provider_memory.success(provider)

        monitor.finish(provider)


    def ai_failed(self, provider, error):

        provider_memory.failed(provider)

        monitor.fail(error)


    def shutdown(self):

        print("=" * 60)

        print("MASTER ENGINE SHUTDOWN")

        print("=" * 60)

        monitor.summary()

        recovery.report()

        queue_manager.report()

        print("=" * 60)


master_engine = MasterEngine()
