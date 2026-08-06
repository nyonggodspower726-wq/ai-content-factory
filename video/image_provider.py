import os
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

from video.visual_style import PROMPTPROHUB_VISUAL_STYLE


POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"



def create_fallback_image(prompt, output_path):

    print("CREATING FALLBACK IMAGE")

    width = 1080
    height = 1920

    image = Image.new(
        "RGB",
        (width, height),
        (18,18,18)
    )

    draw = ImageDraw.Draw(image)

    text = (
        "PromptProHub AI\n\n"
        + prompt[:180]
    )

    try:

        font = ImageFont.truetype(
            "DejaVuSans.ttf",
            52
        )

    except:

        font = ImageFont.load_default()


    draw.multiline_text(
        (80,650),
        text,
        fill=(255,255,255),
        font=font,
        spacing=18
    )


    image.save(output_path)

    return output_path



def generate_ai_image(
    prompt,
    output_folder="assets/images"
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    filename = (
        str(abs(hash(prompt)))
        + ".png"
    )


    image_path = os.path.join(
        output_folder,
        filename
    )


    if os.path.exists(image_path):

        print(
            "Using cached image:",
            image_path
        )

        return image_path



    print("="*60)
    print("GENERATING PROMPTPROHUB REALISTIC IMAGE")
    print("="*60)



    final_prompt = f"""

{PROMPTPROHUB_VISUAL_STYLE}


SCENE:

{prompt}

"""


    url = (
        POLLINATIONS_URL
        +
        urllib.parse.quote(
            final_prompt
        )
    )


    try:

        response = requests.get(
            url,
            timeout=300
        )


        response.raise_for_status()


        with open(
            image_path,
            "wb"
        ) as f:

            f.write(
                response.content
            )


        print(
            "IMAGE CREATED:",
            image_path
        )


        return image_path



    except Exception as e:

        print(
            "POLLINATIONS FAILED:",
            e
        )


        return create_fallback_image(
            prompt,
            image_path
)
