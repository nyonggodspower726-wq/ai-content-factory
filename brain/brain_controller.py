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
from brain.retention_engine import choose_retention
from brain.cta_engine import choose_cta
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
        topic
    ):

        print("=" * 60)
        print("BUILDING AI CAMPAIGN")
        print("=" * 60)

        project = {
            "topic": topic
        }

        print(
            "FINAL CREATIVE TOPIC:",
            topic
        )

        # =====================================
        # PRODUCT
        # =====================================

        project["product"] = self.safe_run(
            "Product Engine",
            recommend_product,
            topic
        )

        # =====================================
        # CEO
        # =====================================

        project["ceo"] = self.safe_run(
            "CEO Engine",
            ceo.review,
            topic,
            project["product"]
        )

        # =====================================
        # BRAND
        # =====================================

        project["brand"] = self.safe_run(
            "Brand Engine",
            brand.get_brand
        )

        # =====================================
        # TREND
        # =====================================

        project["trend"] = self.safe_run(
            "Market Trend Engine",
            discover_trends,
            topic
        )

        # =====================================
        # AUDIENCE
        # =====================================

        project["audience"] = self.safe_run(
            "Audience Engine",
            audience_plan,
            topic
        )

        # =====================================
        # OFFER
        # =====================================

        project["offer"] = self.safe_run(
            "Offer Engine",
            create_offer,
            project["product"],
            project["audience"]
        )

        # =====================================
        # THINKING
        # =====================================

        project["thinking"] = self.safe_run(
            "Thinking Engine",
            think,
            project["product"],
            topic
        )

        # =====================================
        # MARKETING
        # =====================================

        project["marketing"] = self.safe_run(
            "Marketing Engine",
            marketing_plan,
            project
        )

        # =====================================
        # PSYCHOLOGY
        # =====================================

        project["psychology"] = self.safe_run(
            "Psychology Engine",
            psychology_plan,
            project["marketing"]
        )

        # =====================================
        # DIRECTOR
        # =====================================

        project["director"] = self.safe_run(
            "Director Engine",
            create_director_plan,
            project
        )

        # =====================================
        # STORYBOARD
        # =====================================

        project["storyboard"] = self.safe_run(
            "Storyboard Engine",
            create_storyboard,
            project["director"]
        )

        # =====================================
        # SCENE PROMPTS
        # =====================================

        project["scene_prompts"] = self.safe_run(
            "Scene Prompt Engine",
            generate_scene_prompts,
            project["storyboard"]
        )

        # =====================================
        # CTA
        # =====================================

        print("=" * 60)
        print("GENERATING CTA BEFORE SCRIPT")
        print("=" * 60)

        project["cta"] = self.safe_run(
            "CTA Engine",
            choose_cta,
            topic
        )

        # =====================================
        # SCRIPT
        # =====================================

        print("=" * 60)
        print("GENERATING SCRIPT WITH CTA")
        print("=" * 60)

        project["script"] = self.safe_run(
            "Script Engine",
            generate_script,
            project,
            project["cta"]
        )

        # =====================================
        # WATCH TIME OPTIMIZATION
        # =====================================

        project["retention"] = self.safe_run(
            "Retention Engine",
            choose_retention,
            topic
        )

        # =====================================
        # VIRAL CHECK
        # =====================================

        project["viral"] = self.safe_run(
            "Viral Analysis Engine",
            evaluate_video,
            project["storyboard"]
        )

        # =====================================
        # FINAL DECISION
        # =====================================

        project["decision"] = self.safe_run(
            "Final Decision Engine",
            final_decision,
            project
        )

        # =====================================
        # COMPLETE
        # =====================================

        print("=" * 60)
        print("BRAIN CAMPAIGN COMPLETE")
        print("=" * 60)

        print(
            "CTA:",
            project.get("cta", "")
        )

        print(
            "SCRIPT GENERATED:",
            bool(project.get("script"))
        )

        return project


brain = BrainController()
