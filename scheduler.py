import time
from datetime import datetime, timezone, timedelta

from bot import main


POSTING_TIMES = [
    "03:44",
    
]


def start_scheduler():

    print("AI CONTENT FACTORY SCHEDULER STARTED")

    completed = []

    while True:

        nigeria_time = datetime.now(timezone(timedelta(hours=1)))
        current_time = nigeria_time.strftime("%H:%M")

        print(f"Scheduler running | Nigeria time: {current_time}")

        if current_time in POSTING_TIMES and current_time not in completed:

            print(f"Starting video generation: {current_time}")

            try:
                main()
                print("Video task completed successfully.")

            except Exception as e:
                print(f"Video task failed: {e}")

            completed.append(current_time)

        if current_time == "00:00":
            completed.clear()

        time.sleep(60)


if __name__ == "__main__":
    start_scheduler()
