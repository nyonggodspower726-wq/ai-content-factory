from brain.pipeline import pipeline

from brain.script_engine import generate_script
from brain.voice_engine import generate_voice as create_voice_profile

from video.voice_generator import generate_voice as create_audio



class ProductionManager:


    def __init__(self):

        print(
            "PromptProHub AI Studio Brain Online"
        )


    def produce(self, topic):

        print("=" * 60)
        print("PROMPTPROHUB AI PRODUCTION MANAGER")
        print("=" * 60)

        print(
            f"Campaign Topic: {topic}"
        )


        try:

            # ==========================
            # STRATEGY PIPELINE
            # ==========================

            print(
                "Running AI Strategy Pipeline..."
            )


            project = pipeline.run(
                topic
            )


            if not project:

                print(
                    "Pipeline returned nothing."
                )

                return None



            # ==========================
            # SCRIPT
            # ==========================

            print(
                "Generating Script..."
            )


            script = generate_script(
                project
            )



            # ==========================
            # VOICE PROFILE
            # ==========================

            print(
                "Generating Voice Profile..."
            )


            voice_profile = create_voice_profile(
                project
            )



            # ==========================
            # AI VOICE
            # ==========================

            print(
                "Generating AI Voice..."
            )


            voice_file = create_audio(

                script,

                voice_profile

            )



            result = {

                "topic": topic,

                "project": project,

                "script": script,

                "voice_profile": voice_profile,

                "voice": voice_file,

                "status": "READY FOR VIDEO"

            }


            print("=" * 60)
            print(
                "PRODUCTION PLAN READY"
            )
            print("=" * 60)


            return result



        except Exception as e:


            print("=" * 60)
            print(
                "PRODUCTION MANAGER FAILED"
            )
            print("=" * 60)

            print(e)


            return None




production = ProductionManager()
