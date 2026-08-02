import schedule
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot import main


def run_bot():

    print("=" * 60)
    print("Starting AI Content Factory...")
    print("=" * 60)

    try:
        main()

        print("VIDEO TASK COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"BOT ERROR: {e}")


def start_scheduler():

    # TEST TIME
    schedule.every().day.at("04:11").do(run_bot)

    # Production later:
    # schedule.every().day.at("09:00").do(run_bot)
    # schedule.every().day.at("14:00").do(run_bot)
    # schedule.every().day.at("20:00").do(run_bot)


    print("AI CONTENT FACTORY SCHEDULER STARTED")


    while True:

        nigeria_time = datetime.now(
            ZoneInfo("Africa/Lagos")
        ).strftime("%H:%M:%S")


        print(
            f"Scheduler running | Nigeria time: {nigeria_time}"
        )


        schedule.run_pending()

        time.sleep(10)
