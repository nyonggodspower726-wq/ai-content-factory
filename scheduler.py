import time
from datetime import datetime
from zoneinfo import ZoneInfo
from bot import main

TIMEZONE = "Africa/Lagos"

SCHEDULE = [
    ("08:00", "tiktok", 1),
    ("09:00", "instagram", 1),
    ("10:00", "youtube", 1),
    ("12:00", "tiktok", 2),
    ("13:00", "instagram", 2),
    ("14:00", "youtube", 2),
    ("16:00", "tiktok", 3),
    ("17:00", "instagram", 3),
    ("18:00", "youtube", 3),
    ("20:00", "tiktok", 4),
    ("21:00", "instagram", 4),
    ("22:00", "youtube", 4),
]

def run_bot(platform, video_number):
    print("=" * 60)
    print("SCHEDULE TRIGGERED")
    print("=" * 60)
    print(f"Platform: {platform.upper()}")
    print(f"Video: {video_number}/4")
    print("=" * 60)
    try:
        result = main(
            platform=platform,
            video_number=video_number
        )
        if result:
            print("=" * 60)
            print("VIDEO TASK COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print(f"Platform: {platform}")
            print(f"Video: {video_number}/4")
            print(f"File: {result.get('video')}")
            print("=" * 60)
        else:
            print("=" * 60)
            print("VIDEO TASK FAILED")
            print("=" * 60)
    except Exception as e:
        print("=" * 60)
        print("BOT ERROR")
        print("=" * 60)
        print(f"Platform: {platform}")
        print(f"Video: {video_number}/4")
        print(f"Error: {e}")
        print("=" * 60)

def start_scheduler():
    print("=" * 60)
    print("PROMPTPROHUB 12-VIDEO SCHEDULER ONLINE")
    print("=" * 60)
    print(f"Timezone: {TIMEZONE}")
    print("Videos per day: 12")
    print("TikTok: 4")
    print("Instagram: 4")
    print("YouTube: 4")
    print("=" * 60)
    print("DAILY SCHEDULE")
    print("=" * 60)
    for schedule_time, platform, video_number in SCHEDULE:
        print(
            f"{schedule_time} -> "
            f"{platform.upper()} #{video_number}"
        )
    print("=" * 60)
    last_run_key = None
    while True:
        now = datetime.now(
            ZoneInfo(TIMEZONE)
        )
        current_date = now.strftime(
            "%Y-%m-%d"
        )
        current_time = now.strftime(
            "%H:%M"
        )
        current_seconds = now.strftime(
            "%H:%M:%S"
        )
        print(
            f"Scheduler running | "
            f"Nigeria time: "
            f"{current_date} "
            f"{current_seconds}"
        )
        for schedule_time, platform, video_number in SCHEDULE:
            run_key = (
                f"{current_date}_"
                f"{schedule_time}_"
                f"{platform}_"
                f"{video_number}"
            )
            if (
                current_time == schedule_time
                and last_run_key != run_key
            ):
                print("=" * 60)
                print(
                    f"POSTING TIME REACHED: "
                    f"{schedule_time}"
                )
                print(
                    f"PLATFORM: "
                    f"{platform.upper()}"
                )
                print(
                    f"VIDEO: "
                    f"{video_number}/4"
                )
                print("=" * 60)
                run_bot(
                    platform,
                    video_number
                )
                last_run_key = run_key
                break
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
