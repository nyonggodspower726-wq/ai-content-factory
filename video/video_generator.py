import os

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


# ==========================================
# DOWNLOAD AI GENERATED SCENES
# ==========================================

def download_ai_videos(video_urls):

    os.makedirs(
        "output/scenes",
        exist_ok=True
    )

    downloaded = []


    for index, url in enumerate(video_urls):

        filename = (
            f"output/scenes/scene_{index}.mp4"
        )


        try:

            import requests


            response = requests.get(
                url,
                stream=True,
                timeout=120
            )


            response.raise_for_status()


            with open(filename, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:
                        file.write(chunk)


            # Validate video

            clip = VideoFileClip(
                filename
            )

            clip.get_frame(0)

            clip.close()


            downloaded.append(
                filename
            )


            print(
                f"AI scene {index + 1} downloaded"
            )


        except Exception as e:

            print(
                f"Scene download failed: {e}"
            )


            if os.path.exists(filename):

                os.remove(filename)


    return downloaded



# ==========================================
# BUILD AI SCENE VIDEO
# ==========================================

def build_scene_video(scene_files):

    clips = []


    for file in scene_files:

        try:

            clip = VideoFileClip(
                file
            )


            clip = clip.resize(
                height=1280
            )


            clips.append(
                clip
            )


        except Exception as e:

            print(
                f"Scene loading error: {e}"
            )


    if len(clips) == 0:

        return None
    final_video = concatenate_videoclips(
        clips,
        method="compose"
    )


    return final_video



# ==========================================
# ADD BACKGROUND MUSIC
# ==========================================

def add_background_music(video, music_file):

    if not music_file:

        return video


    if not os.path.exists(music_file):

        print(
            "Music file not found"
        )

        return video


    try:

        voice = video.audio


        music = AudioFileClip(
            music_file
        )


        music = music.volumex(
            0.12
        )


        music = music.set_duration(
            video.duration
        )


        final_audio = CompositeAudioClip(
            [
                music,
                voice
            ]
        )


        video = video.set_audio(
            final_audio
        )


        print(
            "Background music added"
        )


        return video


    except Exception as e:

        print(
            f"Music error: {e}"
        )


        return video



# ==========================================
# CREATE AI GENERATED VIDEO
# ==========================================

def create_video(
    prompts,
    script,
    voice_file
):

    print(
        "Starting AI Video Production..."
    )


    try:

        print(
            "Generating AI scenes..."
        )


        ai_scenes = generate_all_scenes(
            prompts
        )


        if len(ai_scenes) == 0:

            print(
                "No AI scenes generated"
            )

            return None



        print(
            "Downloading AI scenes..."
        )


        scene_files = download_ai_videos(
            ai_scenes
        )


        if len(scene_files) == 0:

            print(
                "No valid scenes found"
            )

            return None
