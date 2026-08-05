import os

from moviepy.editor import (
    AudioFileClip,
    CompositeAudioClip
)


def add_background_music(

    video,

    music_path,

    volume=0.15

):

    print("=" * 60)
    print("BACKGROUND MUSIC ENGINE")
    print("=" * 60)

    if video is None:

        print("No video received.")

        return None

    if not music_path:

        print("No music selected.")

        return video

    if not os.path.exists(music_path):

        print("Music file not found.")

        return video

    try:

        music = AudioFileClip(
            music_path
        )

        music = music.volumex(
            volume
        )

        music = music.set_duration(
            video.duration
        )

        if video.audio:

            final_audio = CompositeAudioClip(

                [

                    video.audio,

                    music

                ]

            )

        else:

            final_audio = music

        video = video.set_audio(
            final_audio
        )

        print("Background music added.")

        return video

    except Exception as e:

        print(

            f"Music Engine Error: {e}"

        )

        return video
