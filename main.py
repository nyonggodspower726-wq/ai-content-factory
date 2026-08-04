from scheduler import start_scheduler


print("=" * 60)
print("PROMPTPROHUB AI CONTENT FACTORY v1.0")
print("=" * 60)


try:

    print("Starting Scheduler...")

    start_scheduler()


except Exception as e:

    print("=" * 60)
    print("FACTORY START FAILED")
    print("=" * 60)

    print(e)
