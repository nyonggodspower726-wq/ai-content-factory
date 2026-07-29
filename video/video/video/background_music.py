from moviepy.editor import AudioFileClip, CompositeAudioClip


def add_background_music(video, music_path, volume=0.15):
    """
    Adds low-volume background music.
    """

    music = AudioFileClip(music_path)

    music = music.volumex(volume)

    music = music.set_duration(video.duration)

    if video.audio:

        final_audio = CompositeAudioClip([
            video.audio,
            music
        ])

    else:

        final_audio = music

    return video.set_audio(final_audio)
