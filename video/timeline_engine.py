import os

from moviepy.editor import VideoFileClip


class TimelineEngine:

    def __init__(self):

        print("=" * 60)
        print("TIMELINE ENGINE")
        print("=" * 60)


    def build(self, clips):

        timeline = []

        current_time = 0


        if not clips:

            return timeline


        for index, clip in enumerate(clips):

            duration = clip.get(
                "duration",
                5
            )


            path = clip.get(
                "clip"
            )


            # ---------------------------------
            # Create MoviePy clip object
            # ---------------------------------

            if path and os.path.exists(path):

                try:

                    clip_object = VideoFileClip(
                        path
                    )

                    clip["clip_object"] = clip_object


                except Exception as e:

                    print(
                        f"Clip loading failed: {e}"
                    )

                    clip["clip_object"] = None


            else:

                clip["clip_object"] = None



            clip["scene_id"] = index + 1

            clip["start"] = current_time

            clip["end"] = current_time + duration


            timeline.append(
                clip
            )


            current_time += duration


        print(
            f"Timeline built with {len(timeline)} scenes."
        )


        return timeline
