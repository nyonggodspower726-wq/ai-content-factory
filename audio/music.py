import os
import random


def get_music(mood="cinematic"):

    """
    PromptProHub AI Music Engine

    Music folders:

    assets/music/

        cinematic/
        energetic/
        emotional/
        luxury/
        trailer/

    Supported:

    mp3
    wav
    m4a
    """

    root = "assets/music"

    folder = os.path.join(root, mood.lower())

    supported = (
        ".mp3",
        ".wav",
        ".m4a"
    )

    # ---------------------------------------
    # Mood Folder
    # ---------------------------------------

    if os.path.exists(folder):

        music = [

            os.path.join(folder, file)

            for file in os.listdir(folder)

            if file.lower().endswith(supported)

        ]

        if music:

            selected = random.choice(music)

            print("=" * 60)
            print("PROMPTPROHUB MUSIC ENGINE")
            print("=" * 60)
            print("Mood :", mood)
            print("Selected :", selected)

            return selected

    # ---------------------------------------
    # Legacy Background Music
    # ---------------------------------------

    legacy = "output/music/background_music.mp3"

    if os.path.exists(legacy):

        print("Using legacy background music.")

        return legacy

    print("=" * 60)
    print("No background music found.")
    print("=" * 60)

    return None
