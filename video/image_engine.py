from video.image_provider import generate_ai_image



class ImageEngine:


    def __init__(self):

        print("=" * 60)
        print("PROMPTPROHUB REALISTIC IMAGE ENGINE")
        print("=" * 60)



    def generate(self, scenes):


        if not scenes:

            return []



        print("Generating realistic AI images...")



        results = []



        for scene in scenes:


            prompt = scene.get(
                "prompt",
                ""
            )



            realistic_style = """

REALISTIC PHOTOGRAPHY ONLY.

A real human person.
Real face.
Natural skin texture.
Real office environment.
Real laptop/computer.
Professional business workspace.

Style:
Apple commercial photography,
Forbes business documentary,
Netflix entrepreneurship documentary.

Camera:
Professional DSLR camera,
cinematic framing,
natural lighting,
shallow depth of field.

DO NOT CREATE:
anime,
cartoon,
illustration,
digital painting,
3D render,
avatar,
game character,
fantasy person,
unrealistic face,
robot human.

Ultra realistic,
professional photography,
high detail,
sharp focus,
vertical 9:16.

"""



            final_prompt = (

                realistic_style

                +

                "\nScene:\n"

                +

                prompt

            )



            image = generate_ai_image(

                final_prompt

            )



            scene["image"] = image


            results.append(
                scene
            )



            print(
                f"Scene {scene.get('scene', 'unknown')} image ready."
            )



        print(
            f"{len(results)} realistic images generated."
        )



        return results
