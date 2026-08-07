import PIL.Image

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

        os.makedirs("output", exist_ok=True)

        self.music_folder = "assets/music"

    def get_background_music(self):

        if not os.path.exists(self.music_folder):

            return None

        music = [

            os.path.join(self.music_folder, f)

            for f in os.listdir(self.music_folder)

            if f.lower().endswith(".mp3")

        ]

        if not music:

            return None

        return random.choice(music)

    def render(

        self,

        timeline,

        voice_file=None

    ):

        if not timeline:

            return None

        clips = []

        for scene in timeline:

            path = scene.get("image")

            if not path:

                continue

            if not os.path.exists(path):

                continue

            duration = scene.get(

                "duration",

                5

            )

            clip = (

                ImageClip(path)

                .set_duration(duration)

                .resize((720, 1280))

            )

            motion = random.choice([

                "zoom_in",

                "zoom_out",

                "slow_zoom"

            ])

            if motion == "zoom_in":

                clip = clip.resize(

                    lambda t: 1 + (

                        0.05 * t / duration

                    )

                )

            elif motion == "zoom_out":

                clip = clip.resize(

                    lambda t: 1.05 - (

                        0.05 * t / duration

                    )

                )

            else:

                clip = clip.resize(

                    lambda t: 1 + (

                        0.03 * t / duration

                    )

                )

            clip = clip.fadein(0.4)

            clip = clip.fadeout(0.4)

            clips.append(clip)

        final = concatenate_videoclips(

            clips,

            method="compose"

        )

        voice = None

        music = None

        tracks = []

        if voice_file and os.path.exists(voice_file):

            voice = AudioFileClip(voice_file)

            tracks.append(voice)

        music_file = self.get_background_music()

        if music_file:

            music = AudioFileClip(music_file)

            music = music.volumex(0.15)

            if music.duration < final.duration:

                music = music.loop(duration=final.duration)

            else:

                music = music.subclip(0, final.duration)

            tracks.append(music)

        if tracks:

            final = final.set_audio(

                CompositeAudioClip(tracks)

            )

        output = "output/ai_sales_video.mp4"

        print("=" * 60)
        print("Rendering Final Video...")
        print("=" * 60)

        final.write_videofile(

            output,

            codec="libx264",

            audio_codec="aac",

            fps=24,

            preset="ultrafast",

            bitrate="2000k",

            threads=1,

            logger=None

        )

        if voice:

            voice.close()

        if music:

            music.close()

        for clip in clips:

            clip.close()

        final.close()

        gc.collect()

        print("=" * 60)
        print("Rendering completed.")
        print(output)
        print("=" * 60)

        return output
