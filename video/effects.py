import subprocess
import os


def add_hook(video_file, text):

    print("Adding professional hook...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    safe_text = (
        text[:80]
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
        .replace("\n", " ")
    )

    drawtext = (
        f"drawtext=text='{safe_text}':"
        "fontsize=60:"
        "fontcolor=white:"
        "borderw=3:"
        "bordercolor=black:"
        "x=(w-text_w)/2:"
        "y=80:"
        "enable='between(t,0,3)',"
        "drawtext=text='Get AI Prompts\\: nyonggodspower726-wq.github.io/promptprohub':"
        "fontsize=28:"
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
        "-vf",
        drawtext,
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
        print("Hook added successfully.")
        return output

    except Exception as e:
        print(f"Hook failed: {e}")
        return video_file
