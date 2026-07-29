import whisper
import os


MODEL = None


def load_model():
    global MODEL

    if MODEL is None:
        print("Loading Whisper model...")
        MODEL = whisper.load_model("base")

    return MODEL


def generate_subtitles(audio_file):

    if not os.path.exists(audio_file):
        raise FileNotFoundError(audio_file)

    print("Generating subtitles...")

    model = load_model()

    result = model.transcribe(
        audio_file,
        fp16=False
    )

    output = "output/subtitles.srt"

    os.makedirs("output", exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:

        for i, seg in enumerate(result["segments"], start=1):

            start = format_time(seg["start"])
            end = format_time(seg["end"])
            text = seg["text"].strip()

            f.write(f"{i}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")

    print("Subtitles saved:", output)

    return output


def format_time(seconds):

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)

    return (
        f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
)
