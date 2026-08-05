from from video.image_engine import ImageEngine
from video.scene_engine import SceneEngine
from video.timeline_engine import TimelineEngine
from video.motion_engine import MotionEngine
from video.transition_engine import TransitionEngine
from video.camera_engine import apply_camera_effects
from video.effects import EffectsEngine
from video.renderer import Renderer
from video.quality_engine import QualityEngine
from video.branding import BrandingEngine
from video.subtitles import add_subtitles
from video.background_music import add_background_music


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
        self.effects_engine = EffectsEngine()
        self.renderer = Renderer()
        self.quality_engine = QualityEngine()
        self.branding_engine = BrandingEngine()

    def generate(
        self,
        prompts,
        script,
        voice_file,
        music_file=None
    ):

        print("=" * 60)
        print("STARTING VIDEO PRODUCTION")
        print("=" * 60)

        # -----------------------------
        # Extract script text
        # -----------------------------
        if isinstance(script, dict):

            script_text = script.get("script", "")

            hook = script.get("hook", "")

        else:

            script_text = str(script)

            hook = script_text.split(".")[0]

        # -----------------------------
        # Scene Creation
        # -----------------------------
        scenes = self.scene_engine.generate(
            prompts,
            script_text
        )

        # -----------------------------
        # Clip Selection
        # -----------------------------
        clips = self.clip_engine.generate(
            scenes
        )

        # -----------------------------
        # Timeline
        # -----------------------------
        timeline = self.timeline_engine.build(
            clips
        )

        # -----------------------------
        # Motion
        # -----------------------------
        timeline = self.motion_engine.apply(
            timeline
        )

        # -----------------------------
        # Camera
        # -----------------------------
        timeline = apply_camera_effects(
            timeline
        )

        # -----------------------------
        # Effects
        # -----------------------------
        timeline = self.effects_engine.apply(
            timeline
        )

        # -----------------------------
        # Transitions
        # -----------------------------
        timeline = self.transition_engine.apply(
            timeline
        )

        # -----------------------------
        # Quality
        # -----------------------------
        timeline = self.quality_engine.optimize(
            timeline
        )

        # -----------------------------
        # Render
        # -----------------------------
        output = self.renderer.render(
            timeline,
            voice_file
        )

        if output is None:

            print("Renderer failed.")

            return None

        # -----------------------------
        # Background Music
        # -----------------------------
        if music_file:

            from moviepy.editor import VideoFileClip

            video = VideoFileClip(output)

            video = add_background_music(
                video,
                music_file
            )

            video.write_videofile(
                "output/music_video.mp4",
                codec="libx264",
                audio_codec="aac",
                fps=30,
                logger=None
            )

            output = "output/music_video.mp4"

        # -----------------------------
        # Subtitles
        # -----------------------------
        output = add_subtitles(
            output,
            script_text
        )

        # -----------------------------
        # Branding
        # -----------------------------
        output = self.branding_engine.apply(
            output,
            hook
        )

        print("=" * 60)
        print("VIDEO PRODUCTION COMPLETED")
        print("=" * 60)

        return output
