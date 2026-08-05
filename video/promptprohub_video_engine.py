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
   def load_clips(self, prompts):

    print("=" * 60)
    print("PROMPTPROHUB CLIP ENGINE")
    print("=" * 60)

    clips = []

    if prompts is None:
        print("No prompts received.")
        return clips

    if isinstance(prompts, str):
        prompts = [prompts]

    for index, prompt in enumerate(prompts):

        print(f"Scene {index + 1}")
        print(f"Prompt: {prompt}")

        scene = {
            "id": index + 1,
            "prompt": prompt,
            "duration": 5,
            "style": "cinematic",
            "camera": "auto",
            "transition": "fade"
        }

        clips.append(scene)

    print(f"Scenes created: {len(clips)}")

    return clips
