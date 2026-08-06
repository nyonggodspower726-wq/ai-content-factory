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



        # =============================
        # MOTION
        # =============================

        print("MOTION ENGINE")


        timeline = self.motion_engine.apply(

            timeline

        )



        # =============================
        # CAMERA
        # =============================

        print("CAMERA ENGINE")


        timeline = apply_camera_effects(

            timeline

        )



        # =============================
        # EFFECTS
        # =============================

        print("EFFECT ENGINE")


        timeline = self.effects_engine.apply(

            timeline

        )



        # =============================
        # TRANSITIONS
        # =============================

        print("TRANSITION ENGINE")


        timeline = self.transition_engine.apply(

            timeline

        )



        # =============================
        # QUALITY
        # =============================

        print("QUALITY ENGINE")


        timeline = self.quality_engine.optimize(

            timeline

        )



        # =============================
        # RENDER
        # =============================

        print("RENDER ENGINE")


        output = self.renderer.render(

            timeline,

            voice_file

        )


        if not self.check_file(
            output,
            "Rendered video"
        ):

            return None




        # =============================
        # MUSIC
        # =============================

        if music_file:


            print(
                "ADDING BACKGROUND MUSIC"
            )


            from moviepy.editor import VideoFileClip


            video = VideoFileClip(
                output
            )


            video = add_background_music(

                video,

                music_file

            )


            music_output = (
                "output/music_video.mp4"
            )


            video.write_videofile(

                music_output,

                codec="libx264",

                audio_codec="aac",

                fps=30,

                logger=None

            )


            video.close()


            output = music_output



            if not self.check_file(
                output,
                "Music video"
            ):

                return None




        # =============================
        # SUBTITLES
        # =============================

        print(
            "SUBTITLE ENGINE"
        )


        output = add_subtitles(

            output,

            script_text

        )



        if not self.check_file(

            output,

            "Subtitle video"

        ):

            return None




        # =============================
        # BRANDING
        # =============================

        print(
            "BRANDING ENGINE"
        )


        output = self.branding_engine.apply(

            output,

            hook

        )



        if not self.check_file(

            output,

            "Final branded video"

        ):

            return None




        print("=" * 60)
        print("FINAL VIDEO READY")
        print(output)
        print("=" * 60)


        return output
