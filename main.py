import threading

from scheduler import start_scheduler
from server import app


def start_server():

    import os

    port = int(os.getenv("PORT", "8080"))

    print("=" * 60)
    print("PROMPTPROHUB VIDEO SERVER STARTING")
    print("=" * 60)
    print("Port:", port)

    app.run(
        host="0.0.0.0",
        port=port,
        threaded=True
    )


print("=" * 60)
print("PROMPTPROHUB AI CONTENT FACTORY v1.0")
print("=" * 60)


try:

    # Start public video server
    server_thread = threading.Thread(
        target=start_server,
        daemon=True
    )

    server_thread.start()


    # Start existing AI scheduler
    print("Starting Scheduler...")

    start_scheduler()


except Exception as e:

    print("=" * 60)
    print("FACTORY START FAILED")
    print("=" * 60)

    print(e)
