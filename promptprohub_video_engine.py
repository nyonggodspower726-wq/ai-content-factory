import os

from video.clip_engine import ClipEngine
from video.scene_engine import SceneEngine
from video.timeline_engine import TimelineEngine
from video.motion_engine import MotionEngine
from video.transition_engine import TransitionEngine
from video.camera_engine import apply_camera_effects
from video.effects import add_hook
from video.subtitles import add_subtitles
from video.renderer import Renderer
from video.quality_engine import QualityEngine

from audio.music import get_music


class PromptProHubVideoEngine:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB VIDEO ENGINE")
        print("=" * 60)

        self.scene_engine = SceneEngine()

        self.clip_engine = ClipEngine()

        self.timeline_engine = TimelineEngine()

        self.motion_engine = MotionEngine()

        self.transition_engine = TransitionEngine()

        self.renderer = Renderer()

        self.quality_engine = QualityEngine()

    def generate(

        self,

        prompts,

        script,

        voice_file

    ):

        print("=" * 60)

        print("STARTING VIDEO PRODUCTION")

        print("=" * 60)

        # ---------------------------------
        # Build scenes
        # ---------------------------------

        scenes = self.scene_engine.generate(

            prompts,

            script

        )

        # ---------------------------------
        # Load clips
        # ---------------------------------

        clips = self.clip_engine.generate(

            scenes

        )

        # ---------------------------------
        # Build timeline
        # ---------------------------------

        timeline = self.timeline_engine.build(

            clips

        )

        # ---------------------------------
        # Camera Engine
        # ---------------------------------

        timeline = apply_camera_effects(

            timeline

        )

        # ---------------------------------
        # Motion Engine
        # ---------------------------------

        timeline = self.motion_engine.apply(

            timeline

        )

        # ---------------------------------
        # Transition Engine
        # ---------------------------------

        timeline = self.transition_engine.apply(

            timeline

        )

        # ---------------------------------
        # Quality Optimizer
        # ---------------------------------

        timeline = self.quality_engine.optimize(

            timeline

        )

        # ---------------------------------
        # Render
        # ---------------------------------

        output = self.renderer.render(

            timeline,

            voice_file

        )

        # ---------------------------------
        # Subtitles
        # ---------------------------------

        output = add_subtitles(

            output,

            script

        )

        # ---------------------------------
        # Branding
        # ---------------------------------

        hook = script.split(".")[0]

        output = add_hook(

            output,

            hook

        )

        print("=" * 60)

        print("VIDEO COMPLETED")

        print("=" * 60)

        return output
