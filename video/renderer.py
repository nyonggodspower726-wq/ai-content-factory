import PIL.Image

# =====================================================
# Pillow Compatibility Fix
# =====================================================
if not hasattr(PIL.Image, "ANTIALIAS"):
    try:
        PIL.Image.ANTIALIAS = PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

import os
import gc
import random

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips
)


class Renderer:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB CINEMATIC RENDER ENGINE")
        print("=" * 60)

        os.makedirs(
            "output",
            exist_ok=True
        )

        self.music_folder = "assets/music"

        os.makedirs(
            self.music_folder,
            exist_ok=True
        )


    def get_background_music(self):

        os.makedirs(
            self.music_folder,
            exist_ok=True
        )

        music = [

            os.path.join(
                self.music_folder,
                file
            )

            for file in os.listdir(
                self.music_folder
            )

            if file.lower().endswith(".mp3")

        ]


        if not music:

            print("=" * 60)
            print("NO BACKGROUND MUSIC FOUND")
            print("=" * 60)

            return None


        return random.choice(music)



    def render(

        self,

        timeline,

        voice_file=None

    ):


        if not timeline:

            print("No timeline.")

            return None



        clips = []



        for scene in timeline:


            path = scene.get(
                "image"
            )


            if not path:

                continue



            if not os.path.exists(path):

                print(
                    f"Missing image: {path}"
                )

                continue



            try:


                duration = scene.get(
                    "duration",
                    5
                )


                clip = (

                    ImageClip(path)

                    .set_duration(
                        duration
                    )

                    .resize(
                        (720,1280)
                    )

                )


                motion = random.choice([

                    "zoom_in",

                    "zoom_out",

                    "slow_zoom"

                ])



                if motion == "zoom_in":


                    clip = clip.resize(

                        lambda t:

                        1 + (
                            0.05 * t / duration
                        )

                    )


                elif motion == "zoom_out":


                    clip = clip.resize(

                        lambda t:

                        1.05 - (
                            0.05 * t / duration
                        )

                    )


                else:


                    clip = clip.resize(

                        lambda t:

                        1 + (
                            0.03 * t / duration
                        )

                    )


                clip = clip.fadein(
                    0.4
                )

                clip = clip.fadeout(
                    0.4
                )


                clips.append(
                    clip
                )


            except Exception as e:


                print(
                    "Renderer Error:",
                    e
                    )
