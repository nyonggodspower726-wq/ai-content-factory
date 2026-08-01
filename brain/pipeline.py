from brain.brand_engine import brand
from brain.audience_engine import analyse_audience
from brain.trend_engine import discover_trends
from brain.product_engine import recommend_product
from brain.offer_engine import create_offer
from brain.marketing_engine import marketing_plan
from brain.psychology import psychology_plan
from brain.director import create_director_plan
from brain.script_engine import generate_script
from brain.storyboard import create_storyboard
from brain.prompt_engine import generate_scene_prompts
from brain.camera_engine import apply_camera
from brain.consistency_engine import ConsistencyEngine
from brain.viral_engine import evaluate_video
from brain.decision_engine import final_decision
from brain.voice_engine import generate_voice
from brain.memory_engine import memory


class Pipeline:

    def __init__(self):

        print("PromptProHub AI Sales Brain Ready")

        self.consistency = ConsistencyEngine()


    def execute(self, topic):

        print("Loading Brand...")

        brand_data = brand.get_brand()


        print("Analysing Audience...")

        audience = analyse_audience(topic)


        print("Finding Trends...")

        trends = discover_trends(topic)


        print("Selecting Product...")

        product = recommend_product(topic)


        print("Creating Offer...")

        offer = create_offer(topic)


        print("Creating Marketing Strategy...")

        marketing = marketing_plan(topic)


        print("Analysing Psychology...")

        psychology = psychology_plan(
            marketing
        )


        print("Creating Director Plan...")

        director = create_director_plan(topic)


        project = {

            "brand": brand_data,

            "audience": audience,

            "trend": trends,

            "product": product,

            "offer": offer,

            "marketing": marketing,

            "psychology": psychology,

            "director": director

        }


        print("Writing Sales Script...")

        script = generate_script(
            project
        )


        project["script"] = script


        print("Creating Storyboard...")

        storyboard = create_storyboard(
            project
        )


        project["storyboard"] = storyboard


        print("Generating Scene Prompts...")

        prompts = generate_scene_prompts(
            storyboard
        )


        print("Applying Cinematic Camera...")

        cinematic_prompts = []

        for prompt in [prompts]:

            camera_prompt = apply_camera(
                str(prompt)
            )

            consistent_prompt = self.consistency.apply(
                camera_prompt
            )

            cinematic_prompts.append(
                consistent_prompt
            )


        project["prompts"] = cinematic_prompts


        print("Checking Viral Potential...")

        viral = evaluate_video(
            project
        )


        project["viral"] = viral


        print("Making Final Decision...")

        decision = final_decision(
            project
        )


        project["decision"] = decision


        print("Creating Voice Plan...")

        voice = generate_voice(
            project
        )


        project["voice"] = voice


        print("Saving Memory...")

        memory.save(
            topic,
            project
        )


        print("AI Brain Completed Successfully")


        return project



pipeline = Pipeline()
