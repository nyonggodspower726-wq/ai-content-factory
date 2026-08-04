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
        print("PROMPTPROHUB AI STUDIO BRAIN ONLINE")
        print("=" * 60)

    def build(self, topic):

        project = {}

        print("CEO")

        # Product Recommendation
        product = recommend_product(topic)
        project["product"] = product

        # CEO Planning
        project["ceo"] = ceo.review(
            topic,
            product
        )

        print("Brand")
        project["brand"] = brand.get_brand()

        print("Trend")
        project["trend"] = discover_trends(topic)

        print("Audience")
        project["audience"] = audience_plan(topic)

        print("Offer")
        project["offer"] = create_offer(
            project["product"],
            project["audience"]
        )

        print("Thinking")
        project["thinking"] = think(
            project["product"],
            topic
        )

        print("Marketing")
        project["marketing"] = marketing_plan(
            project["thinking"]
        )

        print("Psychology")
        project["psychology"] = psychology_plan(
            project["marketing"]
        )

        print("Director")
        project["director"] = create_director_plan(
            project["thinking"]
        )

        print("Storyboard")
        project["storyboard"] = create_storyboard(
            project["director"]
        )

        print("Scene Prompts")
        project["scene_prompts"] = generate_scene_prompts(
            project["storyboard"]
        )

        print("Script")
        project["script"] = generate_script(
            project
        )

        print("Viral Analysis")
        project["viral"] = evaluate_video(
            project["storyboard"]
        )

        print("Decision")
        project["decision"] = final_decision(
            project
        )

        return project


brain = BrainController()
