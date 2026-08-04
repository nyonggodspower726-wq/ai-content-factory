import os
import requests

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from video.ai_video_worker import generate_all_scenes
from video.effects import add_hook
from video.subtitles import add_subtitles
from audio.music import get_music


# ============================================================
# DOWNLOAD AI GENERATED SCENES
# Supports:
# - WAN
# - FAL
# - MiniMax
# - CogVideo
# - LTX
# ============================================================

def download_ai_videos(video_urls):

    os.makedirs(
        "output/scenes",
        exist_ok=True
    )

    downloaded = []

    if not video_urls:

        print("=" * 60)
        print("No AI videos returned.")
        print("=" * 60)

        return downloaded

    for index, item in enumerate(video_urls):

        filename = f"output/scenes/scene_{index}.mp4"

        try:

            url = None

            # -----------------------------
            # Dictionary response
            # -----------------------------
            if isinstance(item, dict):

                # video -> {url: ...}
                if item.get("video"):

                    if isinstance(item["video"], dict):

                        url = item["video"].get("url")

                    else:

                        url = item["video"]

                # direct url
                elif item.get("url"):

                    url = item["url"]

                else:

                    print(
                        f"Scene {index+1}: invalid response"
                    )

                    print(item)

                    continue

            # -----------------------------
            # String response
            # -----------------------------
            elif isinstance(item, str):

                url = item

            else:

                print(
                    f"Scene {index+1}: unsupported response"
                )

                print(type(item))

                continue

            # -----------------------------
            # Empty URL
            # -----------------------------
            if not url:

                print(
                    f"Scene {index+1}: missing URL"
                )

                continue

            print(
                f"Downloading Scene {index+1}"
            )

            response = requests.get(

                url,

                stream=True,

                timeout=180

            )

            response.raise_for_status()

            with open(
                filename,
                "wb"
            ) as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:

                        file.write(chunk)

            # Validate video
            clip = VideoFileClip(filename)

            clip.get_frame(0)

            clip.close()

            downloaded.append(filename)

            print(
                f"Scene {index+1} downloaded."
            )

        except Exception as e:

            print(
                f"Scene {index+1} failed."
            )

            print(e)

            if os.path.exists(filename):

                os.remove(filename)

    return downloaded
# ============================================================
# BUILD SCENE VIDEO
# ============================================================

def build_scene_video(scene_files):

    clips = []

    if not scene_files:

        print("No scene files available.")

        return None

    for file in scene_files:

        try:

            print(f"Loading {file}")

            clip = VideoFileClip(file)

            clip = clip.resize(height=1280)

            clips.append(clip)

        except Exception as e:

            print(f"Scene loading failed: {e}")

    if len(clips) == 0:

        print("No valid video clips.")

        return None

    final_video = concatenate_videoclips(

        clips,

        method="compose"

    )

    return final_video


# ============================================================
# BACKGROUND MUSIC
# ============================================================

def add_background_music(

    video,

    music_file

):

    if video is None:

        return None

    if not music_file:

        print("No music selected.")

        return video

    if not os.path.exists(music_file):

        print("Music file not found.")

        return video

    try:

        voice = video.audio

        music = AudioFileClip(music_file)

        music = music.volumex(0.12)

        music = music.set_duration(video.duration)

        if voice:

            final_audio = CompositeAudioClip(

                [

                    music,

                    voice

                ]

            )

        else:

            final_audio = music

        video = video.set_audio(final_audio)

        print("Background music added.")

        return video

    except Exception as e:

        print(f"Music Error: {e}")

        return video
# ============================================================
# CREATE AI GENERATED VIDEO
# ============================================================

def create_video(

    prompts,

    script,

    voice_file

):

    print("=" * 60)
    print("PROMPTPROHUB AI VIDEO STUDIO")
    print("=" * 60)

    try:

        print("Generating AI scenes...")

        ai_scenes = generate_all_scenes(
            prompts
        )

        # -----------------------------
        # Safety Check
        # -----------------------------
        if ai_scenes is None:

            print("AI returned None.")

            return None

        if not isinstance(ai_scenes, list):

            print("AI returned invalid format.")

            print(type(ai_scenes))

            return None

        if len(ai_scenes) == 0:

            print("No AI scenes generated.")

            return None

        print("Downloading AI scenes...")

        scene_files = download_ai_videos(
            ai_scenes
        )

        if not scene_files:

            print("No downloadable scenes.")

            return None

        print("Building timeline...")

        video = build_scene_video(
            scene_files
        )

        if video is None:

            print("Timeline creation failed.")

            return None

        print("Adding narration...")

        if (

            voice_file

            and

            os.path.exists(
                voice_file
            )

        ):

            voice = AudioFileClip(
                voice_file
            )

            video = video.set_duration(
                voice.duration
            )

            video = video.set_audio(
                voice
            )

        else:

            print(
                "Voice file missing."
            )

        print(
            "Adding music..."
        )

        music_file = get_music()

        if music_file:

            video = add_background_music(

                video,

                music_file

            )

        output = "output/ai_sales_video.mp4"

        os.makedirs(

            "output",

            exist_ok=True

        )
