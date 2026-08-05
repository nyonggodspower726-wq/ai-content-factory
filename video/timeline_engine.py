class TimelineEngine:

    def __init__(self):

        print("=" * 60)
        print("TIMELINE ENGINE")
        print("=" * 60)

    def build(self, scenes):

        timeline = []

        current_time = 0

        if not scenes:

            return timeline

        for index, scene in enumerate(scenes):

            duration = scene.get(
                "duration",
                5
            )

            scene["scene_id"] = index + 1

            scene["start"] = current_time

            scene["end"] = current_time + duration

            # AI image path
            scene["image"] = scene.get(
                "image"
            )

            timeline.append(
                scene
            )

            current_time += duration

        print(
            f"Timeline built with {len(timeline)} scenes."
        )

        return timeline
