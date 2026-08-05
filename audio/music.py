import os
import random


class MusicEngine:

    def __init__(self):

        self.root = "assets/music"

        self.supported = (
            ".mp3",
            ".wav",
            ".m4a"
        )

        print("=" * 60)
        print("PROMPTPROHUB MUSIC ENGINE")
        print("=" * 60)

    def get_music(self, mood="cinematic"):

        mood = (mood or "cinematic").lower()

        folder = os.path.join(
            self.root,
            mood
        )

        # ------------------------------------
        # Mood Folder
        # ------------------------------------

        if os.path.exists(folder):

            tracks = [

                os.path.join(folder, file)

                for file in os.listdir(folder)

                if file.lower().endswith(
                    self.supported
                )

            ]

            if tracks:

                selected = random.choice(
                    tracks
                )

                print(
                    f"Music Mood : {mood}"
                )

                print(
                    f"Selected : {selected}"
                )

                return selected

        # ------------------------------------
        # Fallback
        # ------------------------------------

        fallback = os.path.join(
            self.root,
            "cinematic"
        )

        if os.path.exists(fallback):

            tracks = [

                os.path.join(fallback, file)

                for file in os.listdir(fallback)

                if file.lower().endswith(
                    self.supported
                )

            ]

            if tracks:

                selected = random.choice(
                    tracks
                )

                print(
                    "Using fallback cinematic music."
                )

                return selected

        # ------------------------------------
        # Legacy
        # ------------------------------------

        legacy = "output/music/background_music.mp3"

        if os.path.exists(legacy):

            print(
                "Using legacy background music."
            )

            return legacy

        print("=" * 60)
        print("NO BACKGROUND MUSIC FOUND")
        print("=" * 60)

        return None


music_engine = MusicEngine()


def get_music(mood="cinematic"):

    return music_engine.get_music(mood)
