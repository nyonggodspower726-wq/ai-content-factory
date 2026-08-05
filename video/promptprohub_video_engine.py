import os

from video.camera_engine import apply_camera_effects
from video.effects import add_hook
from video.subtitles import add_subtitles
from audio.music import get_music


class PromptProHubVideoEngine:

    def __init__(self):
        print("=" * 60)
        print("PROMPTPROHUB VIDEO ENGINE")
        print("=" * 60)

    def generate(
        self,
        prompts,
        script,
        voice_file
    ):

        print("Receiving Brain Engine data...")

        clips = self.load_clips(prompts)

        timeline = self.build_timeline(clips)

        timeline = self.camera_engine(timeline)

        timeline = self.effects_engine(
            timeline,
            script
        )

        timeline = self.music_engine(timeline)

        timeline = self.subtitle_engine(
            timeline,
            script
        )

        final = self.render(timeline)

        return final
