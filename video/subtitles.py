import os
import subprocess


# ==========================================
# CREATE SRT FILE
# ==========================================

def create_srt(script):

    os.makedirs("output", exist_ok=True)

    srt_file = "output/subtitles.srt"

    words = script.split()

    if not words:
        return None

    chunk_size = 6

    duration_per_chunk = 2.5

    with open(srt_file, "w", encoding="utf-8") as f:

        index = 1

        start = 0.0

        for i in range(0, len(words), chunk_size):

            text = " ".join(words[i:i + chunk_size])

            end = start + duration_per_chunk

            f.write(f"{index}\n")
            f.write(
                f"{format_time(start)} --> {format_time(end)}\n"
            )
            f.write(text + "\n\n")

            index += 1
            start = end

    return srt_file
# ==========================================
# FORMAT TIME
# ==========================================

def format_time(seconds):

    hours = int(seconds // 3600)

    minutes = int((seconds % 3600) // 60)

    secs = int(seconds % 60)

    millis = int((seconds - int(seconds)) * 1000)

    return (
        f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
    )


# ==========================================
# ADD SUBTITLES USING FFMPEG
# ==========================================

def add_subtitles(video_file, script):

    srt_file = create_srt(script)

    if srt_file is None:
        return video_file

    output = "output/subtitled_video.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        video_file,
        "-vf",
        (
            f"subtitles={srt_file}:"
            "force_style="
            "'Fontsize=20,"
            "PrimaryColour=&HFFFFFF&,"
            "OutlineColour=&H000000&,"
            "BorderStyle=1,"
            "Outline=2,"
            "Shadow=0,"
            "Alignment=2,"
            "MarginV=80'"
        ),
        "-c:a",
        "copy",
        output
    ]
    try:

        print("Adding subtitles with FFmpeg...")

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

        print("Subtitles added successfully.")

        return output

    except subprocess.CalledProcessError as e:

        print("FFmpeg subtitle error!")

        if e.stderr:
            print(e.stderr)

        return video_file

    except Exception as e:

        print(f"Subtitle error: {e}")

        return video_file
# ==========================================
# END OF FILE
# ==========================================
