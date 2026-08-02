import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot import main


def run_bot():

    print("=" * 60)
    print("SCHEDULER TRIGGERED - STARTING BOT")
    print("=" * 60)

    try:
        main()
        print("VIDEO TASK COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"BOT ERROR: {e}")


def start_scheduler():

    print("AI CONTENT FACTORY SCHEDULER STARTED")

    already_run = False

    while True:

        now = datetime.now(
            ZoneInfo("Africa/Lagos")
        )

        print(
            f"Scheduler running | Nigeria time: {now.strftime('%H:%M:%S')}"
        )

        # TEST: change this time manually
        if (
            now.hour == 17
            and now.minute == 08
            and not already_run
        ):

            run_bot()
            already_run = True


        if now.minute != 34:
            already_run = False


        time.sleep(10)
