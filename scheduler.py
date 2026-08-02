import time
from datetime import datetime, timezone, timedelta

from bot import main


POSTING_TIMES = [
    "03:45",
]


def start_scheduler():

    print("=" * 50)
    print("AI CONTENT FACTORY v1.0")
    print("=" * 50)
    print("AI CONTENT FACTORY SCHEDULER STARTED")

    completed = set()

    while True:

        nigeria_time = datetime.now(
            timezone(timedelta(hours=1))
        )

        current_time = nigeria_time.strftime("%H:%M")

        print(f"Scheduler running | Nigeria time: {current_time}")

        if (
            current_time in POSTING_TIMES
            and current_time not in completed
        ):

            print("=" * 50)
            print(f"Starting video generation: {current_time}")
            print("=" * 50)

            try:

                main()

                print("=" * 50)
                print("VIDEO TASK COMPLETED SUCCESSFULLY")
                print("=" * 50)

            except Exception as e:

                print("=" * 50)
                print("VIDEO TASK FAILED")
                print(type(e).__name__)
                print(str(e))
                print("=" * 50)

            completed.add(current_time)

        # Reset every midnight
        if current_time == "00:00":
            completed.clear()

        # Check every 10 seconds
        time.sleep(10)


if __name__ == "__main__":
    start_scheduler()
