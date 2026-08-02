from brain.brand_engine import brand
from brain.thinking_engine import think
from brain.director import create_director_plan
from brain.marketing_engine import marketing_plan
from brain.psychology import psychology_plan
from brain.storyboard import create_storyboard
from brain.prompt_engine import generate_scene_prompts
from brain.trend_engine import discover_trends
from brain.product_engine import recommend_product
from brain.viral_engine import evaluate_video
from brain.decision_engine import final_decision


class Pipeline:

    def __init__(self):

        print("PromptProHub AI Studio Brain Online")


    def execute(self, topic):

        print("=" * 60)
        print("STEP 1 : BRAND")
        print("=" * 60)

        brand_data = brand.get_brand()


        print("=" * 60)
        print("STEP 2 : TREND BRAIN")
        print("=" * 60)

        trends = discover_trends(topic)


        print("Campaign Topic:")
        print(topic)


        print("=" * 60)
        print("STEP 3 : PRODUCT")
        print("=" * 60)

        product = recommend_product(topic)


        print("=" * 60)
        print("STEP 4 : THINKING BRAIN")
        print("=" * 60)

        thinking = think(product, topic)


        print("=" * 60)
        print("STEP 5 : MARKETING")
        print("=" * 60)

        marketing = marketing_plan(thinking)


        print("=" * 60)
        print("STEP 6 : PSYCHOLOGY")
        print("=" * 60)

        psychology = psychology_plan(marketing)


        print("=" * 60)
        print("STEP 7 : DIRECTOR")
        print("=" * 60)

        director = create_director_plan(thinking)


        print("=" * 60)
        print("STEP 8 : STORYBOARD")
        print("=" * 60)

        storyboard = create_storyboard(director)


        print("=" * 60)
        print("STEP 9 : SCENE PROMPTS")
        print("=" * 60)

        prompts = generate_scene_prompts(storyboard)


        print("=" * 60)
        print("STEP 10 : VIRAL ANALYSIS")
        print("=" * 60)

        viral = evaluate_video(storyboard)


        project = {

            "topic": topic,

            "brand": brand_data,

            "trend": trends,

            "product": product,

            "thinking": thinking,

            "marketing": marketing,

            "psychology": psychology,

            "director": director,

            "storyboard": storyboard,

            "scene_prompts": prompts,

            "viral": viral

        }


        print("=" * 60)
        print("STEP 11 : FINAL DECISION")
        print("=" * 60)

        decision = final_decision(project)

        project["decision"] = decision


        return project



pipeline = Pipeline()
