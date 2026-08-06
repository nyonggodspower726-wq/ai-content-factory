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
            "RUNNING PRODUCTION BRAIN SYSTEM"
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
        # VOICE ENGINE
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
        # VIDEO ENGINE
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

        print("=" * 60)
        print("DATABASE ENGINE")
        print("=" * 60)


        database.save(
            project
        )



        # ==========================
        # MEMORY ENGINE
        # ==========================

        print("=" * 60)
        print("MEMORY ENGINE")
        print("=" * 60)


        memory.save(

            topic,

            {

                "video": video,

                "decision":

                project.get(
                    "decision",
                    {}
                ),

                "hook":

                project.get(
                    "hook",
                    ""
                )

            }

        )



        # ==========================
        # QUEUE ENGINE
        # ==========================

        print("=" * 60)
        print("QUEUE ENGINE")
        print("=" * 60)


        queue_manager.complete(
            topic
        )



        # ==========================
        # LEARNING ENGINE
        # ==========================

        print("=" * 60)
        print("LEARNING ENGINE")
        print("=" * 60)


        report = learning.recommend()


        print(report)



        print("=" * 60)
        print("PRODUCTION COMPLETE")
        print("=" * 60)


        return project





controller = ProductionController()
