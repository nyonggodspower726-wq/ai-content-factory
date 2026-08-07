import os

from PIL import Image, ImageDraw, ImageFont

from moviepy.editor import ImageClip


class EndCard:

    def __init__(self):

        self.duration = 6


    def create(self):

        width = 720
        height = 1280

        image = Image.new(
            "RGB",
            (width, height),
            (15, 15, 15)
        )


        draw = ImageDraw.Draw(image)


        try:

            title_font = ImageFont.truetype(
                "DejaVuSans.ttf",
                44
            )

            text_font = ImageFont.truetype(
                "DejaVuSans.ttf",
                36
            )

            small_font = ImageFont.truetype(
                "DejaVuSans.ttf",
                28
            )

        except:

            title_font = None
            text_font = None
            small_font = None



        lines = [

            (
                "Discover smarter",
                title_font,
                300
            ),

            (
                "AI tools and prompts.",
                title_font,
                370
            ),

            (
                "🌐 promptprohub00.netlify.app",
                text_font,
                550
            ),

            (
                "#AI  #ChatGPT",
                small_font,
                750
            ),

            (
                "#Business  #Freelancer",
                small_font,
                810
            ),

            (
                "#PromptProHub",
                small_font,
                870
            )

        ]



        for text, font, y in lines:


            box = draw.textbbox(
                (0, 0),
                text,
                font=font
            )


            text_width = (
                box[2] - box[0]
            )


            x = (
                width - text_width
            ) // 2



            draw.text(

                (x, y),

                text,

                fill="white",

                font=font

            )



        os.makedirs(
            "output",
            exist_ok=True
        )


        image_path = (
            "output/end_card.png"
        )


        image.save(
            image_path
        )



        return (

            ImageClip(image_path)

            .set_duration(
                self.duration
            )

            )
