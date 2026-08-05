from video.clip_engine import ClipEngine
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



        # ===============================
        # SCENE CREATION
        # ===============================

        scenes = self.scene_engine.generate(

            prompts,

            script

        )



        # ===============================
        # CLIP SELECTION
        # ===============================

        clips = self.clip_engine.generate(

            scenes

        )



        # ===============================
        # TIMELINE
        # ===============================

        timeline = self.timeline_engine.build(

            clips

        )



        # ===============================
        # MOTION
        # ===============================

        timeline = self.motion_engine.apply(

            timeline

        )



        # ===============================
        # CAMERA
        # ===============================

        timeline = apply_camera_effects(

            timeline

        )



        # ===============================
        # VISUAL EFFECTS
        # ===============================

        timeline = self.effects_engine.apply(

            timeline

        )



        # ===============================
        # TRANSITIONS
        # ===============================

        timeline = self.transition_engine.apply(

            timeline

        )



        # ===============================
        # QUALITY
        # ===============================

        timeline = self.quality_engine.optimize(

            timeline

        )



        # ===============================
        # RENDER
        # ===============================

        output = self.renderer.render(

            timeline,

            voice_file

        )



        # ===============================
        # MUSIC
        # ===============================

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



        # ===============================
        # SUBTITLES
        # ===============================

        output = add_subtitles(

            output,

            script

        )



        # ===============================
        # BRANDING
        # ===============================

        hook = script.split(".")[0]


        output = self.branding_engine.apply(

            output,

            hook

        )


        print("=" * 60)

        print("VIDEO PRODUCTION COMPLETED")

        print("=" * 60)


        return output
