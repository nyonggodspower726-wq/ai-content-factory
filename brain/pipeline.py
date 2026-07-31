from brain.brand_engine import brand
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

        print("PromptProHub AI Studio Pipeline Ready")


    def execute(self, topic):

        print("Loading Brand...")

        brand_data = brand.get_brand()

        print("Finding Trends...")

        trends = discover_trends(topic)

        print("Selecting Product...")

        product = recommend_product(topic)

        print("Director Planning...")

        director = create_director_plan(topic)

        print("Marketing Planning...")

        marketing = marketing_plan(topic)

        print("Psychology Planning...")

        psychology = psychology_plan(marketing)

        print("Creating Storyboard...")

        storyboard = create_storyboard(director)

        print("Generating Scene Prompts...")

        prompts = generate_scene_prompts(storyboard)

        print("Evaluating Virality...")

        viral = evaluate_video(storyboard)

        project = {

            "brand": brand_data,

            "trend": trends,

            "product": product,

            "director": director,

            "marketing": marketing,

            "psychology": psychology,

            "storyboard": storyboard,

            "prompts": prompts,

            "viral": viral

        }

        decision = final_decision(project)

        project["decision"] = decision

        return project


pipeline = Pipeline()
