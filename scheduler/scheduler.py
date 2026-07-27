import schedule
import time
from bot import main

def run_bot():
    print("Starting AI Content Factory...")
    main()

# First video
schedule.every().day.at("09:00").do(run_bot)

# Second video
schedule.every().day.at("18:00").do(run_bot)

print("Scheduler is running...")

while True:
    schedule.run_pending()
    time.sleep(30)
