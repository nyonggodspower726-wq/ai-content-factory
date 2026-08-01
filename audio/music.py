import os


def get_music():

    """
    PromptProHub AI Music Loader

    For now this function simply checks whether
    an AI-generated background music file already
    exists inside output/music/.

    Later this can be connected to an AI music
    generation engine without changing the rest
    of the system.
    """

    os.makedirs(
        "output/music",
        exist_ok=True
    )

    music_file = "output/music/background_music.mp3"

    if os.path.exists(music_file):

        print(
            "Background music found:",
            music_file
        )

        return music_file

    print(
        "No background music available."
    )

    return None
