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

        print("=" * 60)
        print("STEP 1 : BRAND ENGINE")
        print("=" * 60)

        brand_data = self.run_engine(

            "BRAND ENGINE",

            brand.get_brand

        )

        project["brand"] = brand_data



        print("=" * 60)
        print("STEP 2 : TREND ENGINE")
        print("=" * 60)

        trends = self.run_engine(

            "TREND ENGINE",

            discover_trends,

            topic

        )

        project["trend"] = trends



        print("=" * 60)
        print("STEP 3 : PRODUCT ENGINE")
        print("=" * 60)

        product = self.run_engine(

            "PRODUCT ENGINE",

            recommend_product,

            topic

        )

        project["product"] = product



        print("=" * 60)
        print("STEP 4 : AUDIENCE ENGINE")
        print("=" * 60)

        audience = self.run_engine(

            "AUDIENCE ENGINE",

            audience_plan,

            topic

        )

        project["audience"] = audience



        print("=" * 60)
        print("STEP 5 : THINKING ENGINE")
        print("=" * 60)

        thinking = self.run_engine(

            "THINKING ENGINE",

            think,

            product,

            topic

        )

        project["thinking"] = thinking



        print("=" * 60)
        print("STEP 6 : MARKETING ENGINE")
        print("=" * 60)

        marketing = self.run_engine(

            "MARKETING ENGINE",

            marketing_plan,

            thinking

        )

        project["marketing"] = marketing



        print("=" * 60)
        print("STEP 7 : PSYCHOLOGY ENGINE")
        print("=" * 60)

        psychology = self.run_engine(

            "PSYCHOLOGY ENGINE",

            psychology_plan,

            marketing

        )

        project["psychology"] = psychology



        print("=" * 60)
        print("STEP 8 : OFFER ENGINE")
        print("=" * 60)

        offer = self.run_engine(

            "OFFER ENGINE",

            create_offer,

            product,

            audience

        )

        project["offer"] = offer

        print("=" * 60)
        print("STEP 9 : DIRECTOR ENGINE")
        print("=" * 60)

        director = self.run_engine(

            "DIRECTOR ENGINE",

            create_director_plan,

            thinking

        )

        project["director"] = director



        print("=" * 60)
        print("STEP 10 : CAMERA ENGINE")
        print("=" * 60)

        camera = self.run_engine(

            "CAMERA ENGINE",

            create_camera_plan,

            director

        )

        project["camera"] = camera



        print("=" * 60)
        print("STEP 11 : STORYBOARD ENGINE")
        print("=" * 60)

        storyboard = self.run_engine(

            "STORYBOARD ENGINE",

            create_storyboard,

            director

        )

        project["storyboard"] = storyboard



        print("=" * 60)
        print("STEP 12 : SCENE PROMPT ENGINE")
        print("=" * 60)

        scene_prompts = self.run_engine(

            "PROMPT ENGINE",

            generate_scene_prompts,

            storyboard

        )

        project["scene_prompts"] = scene_prompts



        print("=" * 60)
        print("STEP 13 : VIRAL ENGINE")
        print("=" * 60)

        viral = self.run_engine(

            "VIRAL ENGINE",

            evaluate_video,

            storyboard

        )

        project["viral"] = viral



        print("=" * 60)
        print("STEP 14 : FINAL DECISION ENGINE")
        print("=" * 60)

        decision = self.run_engine(

            "DECISION ENGINE",

            final_decision,

            project

        )

        project["decision"] = decision
