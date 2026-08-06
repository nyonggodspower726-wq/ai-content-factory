from brain.ai_router import ask_ai

from brain.topic_diversity_engine import choose_topic

from brain.trend_brain import generate_trending_ideas

from brain.viral_angle_engine import choose_best_angle

from brain.curiosity_engine import choose_curiosity

from brain.hook_engine import choose_hook

from brain.retention_engine import choose_retention

from brain.cta_engine import choose_cta


from brain.ceo_engine import ceo
from brain.brand_engine import brand
from brain.trend_engine import discover_trends
from brain.product_engine import recommend_product
from brain.audience_engine import audience_plan
from brain.offer_engine import create_offer
from brain.thinking_engine import think
from brain.marketing_engine import marketing_plan
from brain.psychology import psychology_plan
from brain.director import create_director_plan
from brain.storyboard import create_storyboard
from brain.prompt_engine import generate_scene_prompts
from brain.script_engine import generate_script
from brain.viral_engine import evaluate_video
from brain.decision_engine import final_decision



class BrainController:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB AI BRAIN ONLINE")
        print("=" * 60)



    def safe_run(
        self,
        name,
        function,
        *args
    ):

        try:

            print("=" * 60)
            print(name)
            print("=" * 60)

            return function(*args)


        except Exception as e:

            print(
                f"{name} FAILED:",
                e
            )

            return {}



    def build(
        self,
        topic=None
    ):


        print("=" * 60)
        print("BUILDING AI CAMPAIGN")
        print("=" * 60)



        # =====================================
        # CREATIVE BRAIN LAYER
        # =====================================


        if not topic:


            topic = self.safe_run(

                "Topic Diversity Engine",

                choose_topic

            )


        project = {

            "topic": topic

        }


        print(
            "FINAL SELECTED TOPIC:",
            topic
        )



        project["trend_ideas"] = self.safe_run(

            "Trend Brain",

            generate_trending_ideas,

            topic

        )



        project["viral_angle"] = self.safe_run(

            "Viral Angle Engine",

            choose_best_angle,

            topic

        )



        project["curiosity"] = self.safe_run(

            "Curiosity Engine",

            choose_curiosity,

            topic

        )



        project["hook"] = self.safe_run(

            "Hook Engine",

            choose_hook,

            topic,

            project["viral_angle"],

            project["curiosity"]

        )




        # =====================================
        # OLD BRAIN SYSTEM
        # =====================================



        project["product"] = self.safe_run(

            "Product",

            recommend_product,

            topic

        )



        project["ceo"] = self.safe_run(

            "CEO",

            ceo.review,

            topic,

            project["product"]

        )



        project["brand"] = self.safe_run(

            "Brand",

            brand.get_brand

        )



        project["trend"] = self.safe_run(

            "Trend Engine",

            discover_trends,

            topic

        )



        project["audience"] = self.safe_run(

            "Audience",

            audience_plan,

            topic

        )



        project["offer"] = self.safe_run(

            "Offer",

            create_offer,

            project["product"],

            project["audience"]

        )



        project["thinking"] = self.safe_run(

            "Thinking",

            think,

            project["product"],

            topic

        )



        project["marketing"] = self.safe_run(

            "Marketing",

            marketing_plan,

            project

        )



        project["psychology"] = self.safe_run(

            "Psychology",

            psychology_plan,

            project["marketing"]

        )



        project["director"] = self.safe_run(

            "Director",

            create_director_plan,

            project

        )



        project["storyboard"] = self.safe_run(

            "Storyboard",

            create_storyboard,

            project["director"]

        )



        project["scene_prompts"] = self.safe_run(

            "Scene Prompts",

            generate_scene_prompts,

            project["storyboard"]

        )



        project["script"] = self.safe_run(

            "Script",

            generate_script,

            project

        )



        # =====================================
        # RETENTION + CONVERSION LAYER
        # =====================================


        project["retention"] = self.safe_run(

            "Retention Engine",

            choose_retention,

            topic

        )



        project["cta"] = self.safe_run(

            "CTA Engine",

            choose_cta,

            topic

        )



        project["viral"] = self.safe_run(

            "Viral Analysis",

            evaluate_video,

            project["storyboard"]

        )



        project["decision"] = self.safe_run(

            "Final Decision",

            final_decision,

            project

        )



        print("=" * 60)
        print("BRAIN CAMPAIGN COMPLETE")
        print("=" * 60)



        return project





brain = BrainController()
