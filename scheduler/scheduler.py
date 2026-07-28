import time
from datetime import datetime

from bot import main


POSTING_TIMES = [
    "08:00",
    "14:00",
    "20:00"
]


def start_scheduler():

    print("AI CONTENT FACTORY SCHEDULER STARTED")

    completed = []

    while True:

        current_time = datetime.now().strftime("%H:%M")

        if current_time in POSTING_TIMES and current_time not in completed:

            print(f"Running content generation: {current_time}")

            main()

            completed.append(current_time)

            print("Video task completed.")

        # Reset daily
        if current_time == "00:00":
            completed.clear()

        time.sleep(30)


if __name__ == "__main__":
    start_scheduler()
