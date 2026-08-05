class TimelineEngine:

    def __init__(self):

        print("=" * 60)
        print("TIMELINE ENGINE")
        print("=" * 60)

    def build(self, clips):

        timeline = []

        current_time = 0

        if clips is None:

            return timeline

        for clip in clips:

            duration = clip.get("duration", 5)

            clip["start"] = current_time

            clip["end"] = current_time + duration

            timeline.append(clip)

            current_time += duration

        print(f"Timeline built with {len(timeline)} scenes.")

        return timeline
