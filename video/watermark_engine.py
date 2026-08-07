import os
import subprocess


class WatermarkEngine:

    def __init__(self):

        self.watermark = "assets/watermark.png"

    def apply(self, video_path):

        if not os.path.exists(video_path):
            print("Video not found.")
            return video_path

        if not os.path.exists(self.watermark):
            print("Watermark not found.")
            return video_path

        output = "output/watermarked_video.mp4"

        command = [

            "ffmpeg",

            "-y",

            "-i", video_path,

            "-i", self.watermark,

            "-filter_complex",

            "overlay=(main_w-overlay_w)/2:main_h-overlay_h-20",

            "-codec:a",

            "copy",

            output

        ]

        try:

            print("=" * 60)
            print("ADDING PROMPTPROHUB WATERMARK")
            print("=" * 60)

            subprocess.run(
                command,
                check=True
            )

            print("Watermark added successfully.")

            return output

        except Exception as e:

            print(e)

            return video_path
