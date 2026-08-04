import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot import main


# Nigeria time (24-hour format)
TEST_TIME = "16:53"


def run_bot():

    print("=" * 60)
    print("SCHEDULE TRIGGERED")
    print("=" * 60)

    try:

        print("Calling bot.py...")

        main()

        print("=" * 60)
        print("VIDEO TASK COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:

        print("=" * 60)
        print(f"BOT ERROR: {e}")
        print("=" * 60)


def start_scheduler():

    print("=" * 60)
    print("AI CONTENT FACTORY SCHEDULER STARTED")
    print("=" * 60)

    print(f"Scheduled trigger time (Nigeria): {TEST_TIME}")

    last_run = None

    while True:

        nigeria_now = datetime.now(
            ZoneInfo("Africa/Lagos")
        )

        current_time = nigeria_now.strftime("%H:%M")
        current_seconds = nigeria_now.strftime("%H:%M:%S")

        print(
            f"Scheduler running | Nigeria time: {current_seconds}"
        )

        # Run only once during the scheduled minute
        if current_time == TEST_TIME:

            if last_run != current_time:

                run_bot()

                last_run = current_time

        else:

            # Reset after the minute has passed
            last_run = None

        time.sleep(1)
