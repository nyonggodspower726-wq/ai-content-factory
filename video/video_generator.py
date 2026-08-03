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



# ==========================================
# DOWNLOAD AI GENERATED SCENES
# SUPPORTS WAN + FAL/MINIMAX OUTPUT
# ==========================================


def download_ai_videos(video_urls):

    os.makedirs(
        "output/scenes",
        exist_ok=True
    )


    downloaded = []


    for index, item in enumerate(video_urls):

        filename = (
            f"output/scenes/scene_{index}.mp4"
        )


        try:

            # Handle different provider formats

            if isinstance(item, dict):

                if "video" in item:

                    url = item["video"]["url"]


                elif "url" in item:

                    url = item["url"]


                else:

                    print(
                        "Unknown video response format"
                    )

                    continue


            else:

                url = item



            print(
                f"Downloading AI scene {index + 1}"
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



            # Validate video file

            clip = VideoFileClip(
                filename
            )


            clip.get_frame(0)


            clip.close()



            downloaded.append(
                filename
            )


            print(
                f"Scene {index + 1} downloaded successfully"
            )



        except Exception as e:


            print(
                f"Scene {index + 1} download failed:"
            )

            print(e)



            if os.path.exists(filename):

                os.remove(filename)



    return downloaded
