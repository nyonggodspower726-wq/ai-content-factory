import os
import threading

from scheduler import start_scheduler
from server import app


def run_server():

    port = int(os.getenv("PORT", "8080"))

    print("=" * 60)
    print("PROMPTPROHUB VIDEO SERVER ONLINE")
    print("=" * 60)
    print("PORT:", port)

    app.run(
        host="0.0.0.0",
        port=port,
        threaded=True
    )


print("=" * 60)
print("PROMPTPROHUB AI CONTENT FACTORY v1.0")
print("=" * 60)


try:

    server_thread = threading.Thread(
        target=run_server,
        daemon=True
    )

    server_thread.start()

    print("Starting Scheduler...")

    start_scheduler()


except Exception as e:

    print("=" * 60)
    print("FACTORY START FAILED")
    print("=" * 60)

    print(e)
