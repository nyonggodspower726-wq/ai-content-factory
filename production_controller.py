from brain.brain_controller import brain

from voice.voice_engine import generate_voice

from video.video_generator import create_video

from database.database import database

from brain.memory_engine import memory

from brain.learning_engine import learning

from queue_manager import queue_manager

from recovery_manager import recovery


class ProductionController:

    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB PRODUCTION CONTROLLER")
        print("=" * 60)

    def produce(self, topic):

        print("=" * 60)
        print("STARTING PRODUCTION")
        print("=" * 60)

        # --------------------------
        # Brain
        # --------------------------

        project = recovery.execute(

            brain.build,

            topic

        )

        # --------------------------
        # Voice
        # --------------------------

        print("=" * 60)
        print("VOICE ENGINE")
        print("=" * 60)

        voice = recovery.execute(

            generate_voice,

            project["script"]

        )

        project["voice"] = voice

        # --------------------------
        # Video
        # --------------------------

        print("=" * 60)
        print("VIDEO ENGINE")
        print("=" * 60)

        video = recovery.execute(

            create_video,

            project["scene_prompts"],

            project["script"],

            voice

        )

        project["video"] = video

        # --------------------------
        # Save Project
        # --------------------------

        database.save(project)

        # --------------------------
        # Memory
        # --------------------------

        memory.save(

            topic,

            {

                "video": video,

                "decision":

                project["decision"]

            }

        )

        # --------------------------
        # Queue
        # --------------------------

        queue_manager.complete(topic)

        # --------------------------
        # Learning
        # --------------------------

        report = learning.recommend()

        print("=" * 60)
        print("LEARNING REPORT")
        print("=" * 60)

        print(report)

        print("=" * 60)
        print("PRODUCTION COMPLETED")
        print("=" * 60)

        return project


controller = ProductionController()
