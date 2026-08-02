import schedule
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot import main


# TEST TIME (5:58 PM)
TEST_TIME = "18:07"


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

    schedule.clear()

    schedule.every(10).seconds.do(run_bot)

    print(f"Scheduled trigger time (Nigeria): {TEST_TIME}")

    while True:

        nigeria_time = datetime.now(
            ZoneInfo("Africa/Lagos")
        ).strftime("%H:%M:%S")

        print(
            f"Scheduler running | Nigeria time: {nigeria_time}"
        )

        schedule.run_pending()

        time.sleep(1)
