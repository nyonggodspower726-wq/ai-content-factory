from brain.director import create_director_plan
from brain.marketing_engine import marketing_plan
from brain.psychology import psychology_plan
from brain.storyboard import create_storyboard
from brain.prompt_engine import generate_scene_prompts
from brain.viral_engine import evaluate_video


class MasterEngine:

    def __init__(self):

        print("PromptProHub AI Studio Initialized")


    def build(self, topic):

        print("Step 1 : Director")

        director = create_director_plan(topic)

        print("Step 2 : Marketing")

        marketing = marketing_plan(topic)

        print("Step 3 : Psychology")

        psychology = psychology_plan(marketing)

        print("Step 4 : Storyboard")

        storyboard = create_storyboard(director)

        print("Step 5 : Scene Prompts")

        prompts = generate_scene_prompts(storyboard)

        print("Step 6 : Viral Analysis")

        viral = evaluate_video(storyboard)

        return {

            "topic": topic,

            "director": director,

            "marketing": marketing,

            "psychology": psychology,

            "storyboard": storyboard,

            "scene_prompts": prompts,

            "viral": viral

        }


engine = MasterEngine()
