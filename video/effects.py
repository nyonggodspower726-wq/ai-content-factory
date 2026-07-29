import subprocess


def add_hook(video_file, text):

    print("Adding hook text with FFmpeg...")

    output = "output/hook_video.mp4"

    # Clean text for FFmpeg
    safe_text = (
        text
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace("\n", " ")
    )


    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
        "-vf",
        f"drawtext=text='{safe_text}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=80:enable='between(t,0,3)'",
        "-c:a",
        "copy",
        output
    ]


    try:

        subprocess.run(
            command,
            check=True
        )

        print("Hook text added successfully.")

        return output


    except Exception as e:

        print(f"Hook failed: {e}")

        return video_file
