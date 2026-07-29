import subprocess


def add_watermark(video_file):

    print("Adding watermark...")

    output = "output/watermarked_video.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
        "-vf",
        "drawtext=text='AI CONTENT FACTORY':fontsize=35:fontcolor=white:x=w-text_w-30:y=h-text_h-30",
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
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

        print("Watermark added successfully.")

        return output

    except Exception as e:

        print(f"Watermark failed: {e}")

        return video_file
