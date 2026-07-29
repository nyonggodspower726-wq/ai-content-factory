from moviepy.editor import AudioFileClip, CompositeAudioClip


def add_background_music(video, music_path, volume=0.15):

    print("Adding background music...")

    music = AudioFileClip(music_path)

    music = music.volumex(volume)

    music = music.set_duration(
        video.duration
    )

    if video.audio:

        audio = CompositeAudioClip(
            [
                video.audio,
                music
            ]
        )

    else:

        audio = music

    return video.set_audio(audio)
