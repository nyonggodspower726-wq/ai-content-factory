import os
import requests

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from video.ai_video_worker import generate_all_scenes

from video.effects import (
    add_hook,
    apply_camera_effects
)

from video.subtitles import add_subtitles

from audio.music import get_music


# ============================================================
# PROMPTPROHUB AI VIDEO STUDIO
# ============================================================

"""
Pipeline

Brain
    ↓
Scene Generator
    ↓
Download Scenes
    ↓
Camera Engine
    ↓
Timeline Builder
    ↓
Voice
    ↓
Music
    ↓
Subtitles
    ↓
Branding
    ↓
Final Export
"""


# ============================================================
# DOWNLOAD AI GENERATED SCENES
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


            if isinstance(item, dict):

                if item.get("video"):

                    if isinstance(item["video"], dict):

                        url = item["video"].get("url")

                    else:

                        url = item["video"]


                elif item.get("url"):

                    url = item["url"]


                else:

                    print(
                        f"Scene {index+1}: invalid response"
                    )

                    print(item)

                    continue


            elif isinstance(item, str):

                url = item


            else:

                print(
                    f"Scene {index+1}: unsupported response"
                )

                print(type(item))

                continue


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


            with open(filename, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:

                        file.write(chunk)



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
import os
import requests

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from video.ai_video_worker import generate_all_scenes

from video.effects import (
    add_hook,
    apply_camera_effects
)

from video.subtitles import add_subtitles

from audio.music import get_music


# ============================================================
# PROMPTPROHUB AI VIDEO STUDIO
# ============================================================

"""
Pipeline

Brain
    ↓
Scene Generator
    ↓
Download Scenes
    ↓
Camera Engine
    ↓
Timeline Builder
    ↓
Voice
    ↓
Music
    ↓
Subtitles
    ↓
Branding
    ↓
Final Export
"""


# ============================================================
# DOWNLOAD AI GENERATED SCENES
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


            if isinstance(item, dict):

                if item.get("video"):

                    if isinstance(item["video"], dict):

                        url = item["video"].get("url")

                    else:

                        url = item["video"]


                elif item.get("url"):

                    url = item["url"]


                else:

                    print(
                        f"Scene {index+1}: invalid response"
                    )

                    print(item)

                    continue


            elif isinstance(item, str):

                url = item


            else:

                print(
                    f"Scene {index+1}: unsupported response"
                )

                print(type(item))

                continue


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


            with open(filename, "wb") as file:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:

                        file.write(chunk)



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
