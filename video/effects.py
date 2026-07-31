import subprocess
import os


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

        print("Branding failed:", e)

        return video_file
