import subprocess
import os


def add_hook(video_file, text):

    print("Adding ending branding...")

    os.makedirs("output", exist_ok=True)

    output = "output/hook_video.mp4"

    command = [
        "ffmpeg",
        "-y",
        "-i", video_file,
        "-i", "assets/logo.png",

        "-filter_complex",

        # Show logo ONLY during last 4 seconds
        "[0:v][1:v]overlay="
        "(W-w)/2:(H-h)/2:"
        "enable='gte(t,duration-4)',"

        # Website
        "drawtext="
        "text='www.promptprohub.com':"
        "fontsize=42:"
        "fontcolor=white:"
        "borderw=3:"
        "bordercolor=black:"
        "x=(w-text_w)/2:"
        "y=H-180:"
        "enable='gte(t,duration-4)',"

        # Call to action
        "drawtext="
        "text='Get Premium AI Prompts':"
        "fontsize=55:"
        "fontcolor=yellow:"
        "borderw=3:"
        "bordercolor=black:"
        "x=(w-text_w)/2:"
        "y=H-110:"
        "enable='gte(t,duration-4)'",

        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "20",
        "-c:a", "copy",

        output,
    ]

    try:
        subprocess.run(command, check=True)

        print("Ending branding added successfully.")

        return output

    except Exception as e:

        print("Branding failed:", e)

        return video_file
