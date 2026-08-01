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
