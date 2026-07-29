import os


def create_subtitles(script):

    print("Generating subtitles...")

    os.makedirs("output", exist_ok=True)

    subtitle_path = "output/subtitles.srt"

    words = script.split()

    subtitle_duration = 2

    with open(subtitle_path, "w", encoding="utf-8") as f:

        counter = 1
        start = 0

        for i in range(0, len(words), 8):

            end = start + subtitle_duration

            text = " ".join(words[i:i + 8])

            f.write(f"{counter}\n")
            f.write(
                f"00:00:{start:02d},000 --> 00:00:{end:02d},000\n"
            )
            f.write(text + "\n\n")

            counter += 1
            start = end

    print("Subtitle file created.")

    return subtitle_path
