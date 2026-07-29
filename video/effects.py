import subprocess
import os


def add_hook(video_file, text):

    print("Adding professional branding...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    # Make the hook safe for FFmpeg drawtext
    safe_text = (
        text[:80]
        .replace("\\", "\\\\")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace(",", r"\,")
        .replace("[", r"\[")
        .replace("]", r"\]")
        .replace("%", r"\%")
        .replace("\n", " ")
    )
    # Escape the website text separately
    website_text = (
        "Get AI Prompts: nyonggodspower726-wq.github.io/promptprohub"
        .replace("\\", "\\\\")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace(",", r"\,")
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
        "y=80:"
        "enable=between(t\\,0\\,3),"
        f"drawtext=text='{website_text}':"
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

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        print("Professional branding added successfully.")

        return output

    except subprocess.CalledProcessError as e:

        print("FFmpeg failed!")

        if e.stderr:
            print(e.stderr)

        return video_file

    except Exception as e:

        print(f"Hook failed: {e}")

        return video_file
