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

        os.makedirs("output", exist_ok=True)

        # Automatically create the music folder
        self.music_folder = "assets/music"
        os.makedirs(self.music_folder, exist_ok=True)

    def get_background_music(self):

        # Ensure folder always exists
        os.makedirs(self.music_folder, exist_ok=True)

        music = [
            os.path.join(self.music_folder, file)
            for file in os.listdir(self.music_folder)
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

            path = scene.get("image")

            if not path:
                continue

            if not os.path.exists(path):
                print(f"Missing image: {path}")
                continue

            try:

                duration = scene.get(
                    "duration",
                    5
                )

                clip = (
                    ImageClip(path)
                    .set_duration(duration)
                    .resize((720, 1280))
                )

                # Random cinematic motion
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

            except Exception as e:

                print("Renderer Error:", e)

        if not clips:

            print("No images loaded.")
            return None

        try:

            final = concatenate_videoclips(
                clips,
                method="compose"
            )

        except Exception as e:

            print("Concatenation Error:", e)
            return None

        voice = None
        music = None
        tracks = []

        # -------------------------------------------------
        # Voice Track
        # -------------------------------------------------
        if voice_file and os.path.exists(voice_file):

            voice = AudioFileClip(voice_file)
            tracks.append(voice)

        # -------------------------------------------------
        # Background Music
        # -------------------------------------------------
        music_file = self.get_background_music()

        if music_file:

            try:

                music = AudioFileClip(music_file)

                # Lower volume so voice remains clear
                music = music.volumex(0.15)

                if music.duration < final.duration:

                    music = music.loop(
                        duration=final.duration
                    )

                else:

                    music = music.subclip(
                        0,
                        final.duration
                    )

                tracks.append(music)

                print(f"Using background music: {music_file}")

            except Exception as e:

                print("Music Error:", e)

        # -------------------------------------------------
        # Combine Audio
        # -------------------------------------------------
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

        # -------------------------------------------------
        # Cleanup
        # -------------------------------------------------
        if voice:
            voice.close()

        if music:
            music.close()

        for clip in clips:
            clip.close()

        final.close()

        del clips
        del final

        gc.collect()

        print("=" * 60)
        print("Rendering completed.")
        print(output)
        print("=" * 60)

        return output
