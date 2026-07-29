import subprocess
import os


def add_hook(video_file, text):

    print("Adding professional hook...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    # Clean text for FFmpeg
    safe_text = (
        text[:80]
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("%", "\\%")
        .replace("\n", " ")
    )

    drawtext = (
        f"drawtext="
        f"text='{safe_text}':"
        f"fontsize=58:"
        f"fontcolor=white:"
        f"borderw=3:"
        f"bordercolor=black:"
        f"box=1:"
        f"boxcolor=black@0.45:"
        f"boxborderw=15:"
        f"x=(w-text_w)/2:"
        f"y=80:"
        f"enable='between(t,0,3)'"
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

        subprocess.run(
            command,
            check=True
        )

        print("Hook added successfully.")

        return output

    except Exception as e:

        print(f"Hook failed: {e}")

        return video_file
