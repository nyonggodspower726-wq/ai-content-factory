from brain.brand_engine import brand
from brain.trend_engine import discover_trends
from brain.product_engine import recommend_product

from brain.thinking_engine import think
from brain.marketing_engine import marketing_plan
from brain.psychology import psychology_plan

from brain.audience_engine import audience_plan
from brain.offer_engine import create_offer

from brain.director import create_director_plan
from brain.camera_engine import create_camera_plan

from brain.storyboard import create_storyboard
from brain.prompt_engine import generate_scene_prompts

from brain.viral_engine import evaluate_video
from brain.decision_engine import final_decision

from brain.monitor import monitor
from brain.recovery_manager import recovery

from brain.database import database
from brain.memory_engine import memory
from brain.learning_engine import learning

from brain.master_engine import master_engine
from brain.ceo_engine import ceo


class Pipeline:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO PIPELINE V2 ONLINE")
        print("=" * 60)



    def run_engine(self, name, function, *args):

        monitor.start(name)

        try:

            result = recovery.execute(
                function,
                *args
            )

            monitor.finish()

            return result


        except Exception as e:

            monitor.fail(e)

            raise e



    def execute(self, topic):


        print("=" * 60)
        print("NEW AI CAMPAIGN STARTED")
        print("=" * 60)


        master_engine.initialize(topic)


        ceo_plan = self.run_engine(

            "CEO ENGINE",

            ceo.review,

            topic

        )


        project = {


            "topic": topic,


            "ceo": ceo_plan

        }
