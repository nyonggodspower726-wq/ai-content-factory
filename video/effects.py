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
