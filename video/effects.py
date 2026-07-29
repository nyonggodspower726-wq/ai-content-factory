import subprocess
import os


def add_hook(video_file, text):

    print("Adding professional branding...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    safe_text = (
        text[:80]
        .replace("\\", "")
        .replace(":", "")
        .replace("'", "")
        .replace(",", "")
        .replace("%", "")
        .replace("\n", " ")
    )

    filter_complex = (
        "movie=assets/logo.png[logo];"
        "[0:v][logo]overlay=W-w-20:20,"
        f"drawtext=text='{safe_text}':"
        "fontsize=60:"
        "fontcolor=white:"
        "borderw=3:"
        "bordercolor=black:"
        "x=(w-text_w)/2:"
        "y=80,"
        "drawtext=text='Get AI Prompts':"
        "fontsize=30:"
        "fontcolor=yellow:"
        "borderw=2:"
        "bordercolor=black:"
        "x=(w-text_w)/2:"
        "y=h-60"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
        "-filter_complex",
        filter_complex,
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "28",
        "-threads",
        "1",
        "-c:a",
        "copy",
        output
    ]

    try:
        subprocess.run(command, check=True)
        print("Professional branding added successfully.")
        return output

    except Exception as e:
        print("Hook failed:", e)
        return video_file
