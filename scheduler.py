import time
from datetime import datetime
from zoneinfo import ZoneInfo

from bot import main


# ============================================================
# DAILY POSTING SCHEDULE — NIGERIA TIME
# ============================================================

SCHEDULE_TIMES = [
    "09:29",
    "12:00",
    "18:00",
    "23:00",
]


# ============================================================
# RUN BOT
# ============================================================

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
        print("BOT ERROR")
        print("=" * 60)

        print(f"ERROR: {e}")

        print("=" * 60)


# ============================================================
# SCHEDULER
# ============================================================

def start_scheduler():

    print("=" * 60)
    print("AI CONTENT FACTORY SCHEDULER STARTED")
    print("=" * 60)

    print("Timezone: Africa/Lagos")

    print(
        "Daily posting times:",
        ", ".join(SCHEDULE_TIMES)
    )

    print("Posts per day: 4")

    print("=" * 60)

    # Prevent duplicate execution during the same minute
    last_run_date = None
    last_run_time = None

    while True:

        nigeria_now = datetime.now(
            ZoneInfo("Africa/Lagos")
        )

        current_date = nigeria_now.strftime(
            "%Y-%m-%d"
        )

        current_time = nigeria_now.strftime(
            "%H:%M"
        )

        current_seconds = nigeria_now.strftime(
            "%H:%M:%S"
        )

        print(
            f"Scheduler running | "
            f"Nigeria time: {current_date} "
            f"{current_seconds}"
        )

        # ====================================================
        # CHECK SCHEDULED TIME
        # ====================================================

        if current_time in SCHEDULE_TIMES:

            # Make sure this scheduled time
            # only runs once per day.
            if (
                last_run_date != current_date
                or last_run_time != current_time
            ):

                print("=" * 60)

                print(
                    f"POSTING TIME REACHED: "
                    f"{current_time}"
                )

                print("=" * 60)

                run_bot()

                last_run_date = current_date
                last_run_time = current_time

        time.sleep(1)


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    start_scheduler()
