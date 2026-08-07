import os

from video.image_engine import ImageEngine
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
from video.watermark_engine import WatermarkEngine



class PromptProHubVideoEngine:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB VIDEO ENGINE ONLINE")
        print("=" * 60)


        self.scene_engine = SceneEngine()

        self.image_engine = ImageEngine()

        self.timeline_engine = TimelineEngine()

        self.motion_engine = MotionEngine()

        self.transition_engine = TransitionEngine()

        self.effects_engine = EffectsEngine()

        self.renderer = Renderer()

        self.quality_engine = QualityEngine()

        self.branding_engine = BrandingEngine()

        self.watermark_engine = WatermarkEngine()



    def check_file(self, path, name):

        if not path:

            print(
                f"{name} returned nothing"
            )

            return False


        if not os.path.exists(path):

            print(
                f"{name} file missing:",
                path
            )

            return False


        print(
            f"{name} READY:",
            path
        )

        return True



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



        # =============================
        # SCRIPT EXTRACTION
        # =============================

        if isinstance(script, dict):

            script_text = script.get(
                "script",
                ""
            )

            hook = script.get(
                "hook",
                ""
            )


        else:

            script_text = str(script)

            hook = script_text.split(".")[0]



        # =============================
        # SCENES
        # =============================

        print("SCENE ENGINE")

        scenes = self.scene_engine.generate(

            prompts,

            script_text

        )


        if not scenes:

            print(
                "SCENE CREATION FAILED"
            )

            return None



        print(
            "Scenes created:",
            len(scenes)
        )



        # =============================
        # IMAGES
        # =============================

        print("IMAGE ENGINE")


        images = self.image_engine.generate(

            scenes

        )


        if not images:

            print(
                "IMAGE GENERATION FAILED"
            )

            return None



        print(
            "Images generated:",
            len(images)
        )



        # =============================
        # TIMELINE
        # =============================

        print("TIMELINE ENGINE")


        timeline = self.timeline_engine.build(

            images

        )


        if not timeline:

            print(
                "TIMELINE FAILED"
            )

            return None
