from brain.brain_controller import brain

from voice.voice_generator import generate_voice

from video.video_generator import create_video


class ProductionController:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB PRODUCTION CONTROLLER ONLINE")
        print("=" * 60)



    def run(self, topic):

        print("=" * 60)
        print("STARTING PRODUCTION")
        print("=" * 60)


        try:

            # ==========================
            # BRAIN CREATION
            # ==========================

            print("Running Brain System...")

            project = brain.create(topic)


            if not project:

                print("Brain failed")

                return None



            # ==========================
            # VOICE GENERATION
            # ==========================

            print("Generating AI Voice...")


            script = project.get(
                "script",
                ""
            )


            voice_profile = project.get(
                "voice_profile",
                "professional"
            )


            voice_file = generate_voice(

                script,

                voice_profile

            )


            if not voice_file:

                print("Voice generation failed")

                return None



            # ==========================
            # VIDEO GENERATION
            # ==========================

            print("Generating AI Video...")


            prompts = project.get(
                "scene_prompts",
                []
            )


            video_file = create_video(

                prompts,

                script,

                voice_file

            )


            if not video_file:

                print("Video generation failed")

                return None



            project["voice"] = voice_file

            project["video"] = video_file



            print("=" * 60)
            print("PRODUCTION COMPLETE")
            print("=" * 60)


            return project



        except Exception as e:


            print("=" * 60)

            print("PRODUCTION ERROR")

            print(str(e))

            print("=" * 60)


            return None




controller = ProductionController()
