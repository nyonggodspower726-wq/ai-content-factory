import os
import subprocess
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize


# ============================================================
# CAMERA ENGINE
# ============================================================

def apply_camera_effects(video_file):

    print("=" * 60)
    print("PROMPTPROHUB CAMERA ENGINE")
    print("=" * 60)

    output = "output/camera_scene.mp4"

    try:

        clip = VideoFileClip(video_file)

        # Smooth cinematic zoom
        clip = clip.fx(
            resize,
            lambda t: 1 + (0.04 * (t / clip.duration))
        )

        clip.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=clip.fps,

            preset="medium",

            threads=4,

            logger=None

        )

        clip.close()

        print("Camera effects completed.")

        return output

    except Exception as e:

        print("Camera Engine Error")

        print(str(e))

        return video_file


# ============================================================
# ENDING BRANDING
# ============================================================

def add_hook(video_file, text):

    print("Adding ending branding...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    try:

        duration = subprocess.check_output(

            [

                "ffprobe",

                "-v",

                "error",

                "-show_entries",

                "format=duration",

                "-of",

                "default=noprint_wrappers=1:nokey=1",

                video_file,

            ]

        ).decode().strip()

        duration = float(duration)

    except Exception:

        duration = 30

    start_time = max(duration - 4, 0)

    filter_complex = (

        f"[0:v][1:v]overlay=(W-w)/2:(H-h)/2:"

        f"enable='gte(t,{start_time})',"

        f"drawtext=text='www.promptprohub.com':"

        f"fontsize=42:"

        f"fontcolor=white:"

        f"borderw=3:"

        f"bordercolor=black:"

        f"x=(w-text_w)/2:"

        f"y=H-180:"

        f"enable='gte(t,{start_time})',"

        f"drawtext=text='Get Premium AI Prompts':"

        f"fontsize=55:"

        f"fontcolor=yellow:"

        f"borderw=3:"

        f"bordercolor=black:"

        f"x=(w-text_w)/2:"

        f"y=H-110:"

        f"enable='gte(t,{start_time})'"

    )

    command = [

        "ffmpeg",

        "-y",

        "-i",

        video_file,

        "-i",

        "assets/logo.png",

        "-filter_complex",

        filter_complex,

        "-c:v",

        "libx264",

        "-preset",

        "medium",

        "-crf",

        "20",

        "-c:a",

        "copy",

        output,

    ]

    try:

        subprocess.run(command, check=True)

        print("Ending branding added successfully.")

        return output

    except Exception as e:

        print("Branding failed:")

        print(str(e))

        return video_file
