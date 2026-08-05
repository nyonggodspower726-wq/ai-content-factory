import os


class AssetManager:

    def __init__(self):

        self.assets = "assets"

        self.clips = os.path.join(
            self.assets,
            "clips"
        )

        self.music = os.path.join(
            self.assets,
            "music"
        )

        self.images = os.path.join(
            self.assets,
            "images"
        )

        self.logos = os.path.join(
            self.assets,
            "logos"
        )

        self.fonts = os.path.join(
            self.assets,
            "fonts"
        )

        self.cache = os.path.join(
            self.assets,
            "cache"
        )

        self.output = "output"

        self.create_folders()

    def create_folders(self):

        folders = [

            self.assets,

            self.clips,

            self.music,

            self.images,

            self.logos,

            self.fonts,

            self.cache,

            self.output

        ]

        for folder in folders:

            os.makedirs(
                folder,
                exist_ok=True
            )

        print("=" * 60)
        print("ASSET MANAGER READY")
        print("=" * 60)

    def get_clip_folder(self):

        return self.clips

    def get_music_folder(self):

        return self.music

    def get_logo_folder(self):

        return self.logos

    def get_font_folder(self):

        return self.fonts

    def get_cache_folder(self):

        return self.cache

    def get_output_folder(self):

        return self.output
