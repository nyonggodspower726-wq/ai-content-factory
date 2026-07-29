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
