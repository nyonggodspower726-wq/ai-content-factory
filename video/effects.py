import subprocess
import os


def add_hook(video_file, text):

    print("Adding professional branding...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    safe_text = (
        text[:80]
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace(",", "\\,")
        .replace("%", "\\%")
        .replace("\n", " ")
    )

    website = (
        "Get AI Prompts"
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace(",", "\\,")
    )

    command = [
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-i", "assets/logo.png",
        "-filter_complex",
        (
            "[0:v][1:v]overlay=W-w-20:20[tmp1];"
            "[tmp1]"
            f"drawtext=text='{safe_text}':"
            "fontsize=60:"
            "fontcolor=white:"
            "borderw=3:"
            "bordercolor=black:"
            "x=(w-text_w)/2:"
            "y=80:"
            "enable='between(t,0,3)'"
            "[tmp2];"
            "[tmp2]"
            f"drawtext=text='{website}':"
            "fontsize=28:"
            "fontcolor=yellow:"
            "borderw=2:"
            "bordercolor=black:"
            "x=(w-text_w)/2:"
            "y=h-60"
        ),
        "-map", "[tmp2]",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "28",
        "-c:a", "copy",
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
