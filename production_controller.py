from brain.brain_controller import brain

from voice.voice_generator import generate_voice

from video.video_generator import create_video

from database.database import database

from brain.memory_engine import memory

from brain.learning_engine import learning

from brain.queue_manager import queue_manager

from brain.recovery_manager import recovery



class ProductionController:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB PRODUCTION CONTROLLER ONLINE")
        print("=" * 60)



    def produce(self, topic):

        print("=" * 60)
        print("STARTING AI PRODUCTION")
        print("=" * 60)



        # ==========================
        # BRAIN SYSTEM
        # ==========================

        print(
            "RUNNING BRAIN SYSTEM"
        )


        project = recovery.execute(

            brain.build,

            topic

        )


        if not project:

            print(
                "Brain failed."
            )

            return None



        # ==========================
        # VOICE
        # ==========================

        print("=" * 60)
        print("VOICE ENGINE")
        print("=" * 60)


        voice = recovery.execute(

            generate_voice,

            project.get(
                "script",
                ""
            )

        )


        project["voice"] = voice



        # ==========================
        # VIDEO
        # ==========================

        print("=" * 60)
        print("VIDEO ENGINE")
        print("=" * 60)


        video = recovery.execute(

            create_video,

            project.get(
                "scene_prompts",
                []
            ),

            project.get(
                "script",
                ""
            ),

            voice

        )


        project["video"] = video



        # ==========================
        # DATABASE
        # ==========================

        print(
            "Saving project..."
        )


        database.save(
            project
        )



        # ==========================
        # MEMORY
        # ==========================

        memory.save(

            topic,

            {

                "video": video,

                "decision":

                project.get(
                    "decision",
                    {}
                )

            }

        )



        # ==========================
        # QUEUE
        # ==========================

        queue_manager.complete(
            topic
        )



        # ==========================
        # LEARNING
        # ==========================

        report = learning.recommend()


        print("=" * 60)
        print("LEARNING REPORT")
        print("=" * 60)

        print(report)



        print("=" * 60)
        print("PRODUCTION COMPLETE")
        print("=" * 60)



        return project





controller = ProductionController()
