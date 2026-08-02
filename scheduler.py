import schedule
import time
from bot import main


def run_bot():

    print("=" * 60)
    print("STARTING AI CONTENT FACTORY")
    print("=" * 60)

    try:

        main()

        print("VIDEO GENERATION COMPLETED")

    except Exception as e:

        print(f"BOT ERROR: {e}")



# ==============================
# TEST MODE
# ==============================

# Use one time for testing
schedule.every().day.at("12:00").do(run_bot)



# ==============================
# PRODUCTION MODE (3 VIDEOS/DAY)
# ==============================
#
# After testing, replace the line above with:
#
# schedule.every().day.at("09:00").do(run_bot)
# schedule.every().day.at("14:00").do(run_bot)
# schedule.every().day.at("20:00").do(run_bot)



print("AI Content Factory Scheduler Running...")


while True:

    schedule.run_pending()

    time.sleep(30)
