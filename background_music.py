from moviepy.editor import AudioFileClip, CompositeAudioClip


def add_background_music(video, music_file):

    print("Adding background music...")

    try:

        voice = video.audio

        music = AudioFileClip(
            music_file
        )

        # Match music length
        music = music.set_duration(
            video.duration
        )

        # Keep music lower than voice
        music = music.volumex(
            0.15
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


        print("Background music added.")

        return video


    except Exception as e:

        print(f"Music failed: {e}")

        return video
