import os
import requests
from PIL import Image, ImageDraw, ImageFont

from config import HF_API_TOKEN


# ==========================================
# PROMPTPROHUB IMAGE PROVIDER
# ==========================================

HF_IMAGE_API = (
    "https://api-inference.huggingface.co/models/"
    "black-forest-labs/FLUX.1-dev"
)


def create_fallback_image(prompt, output_path):

    print("Creating fallback cinematic image...")

    width = 1080
    height = 1920

    image = Image.new(
        "RGB",
        (width, height),
        (20, 20, 20)
    )

    draw = ImageDraw.Draw(image)

    text = (
        "PromptProHub AI\n\n"
        + prompt[:150]
    )

    try:

        font = ImageFont.truetype(
            "DejaVuSans.ttf",
            55
        )

    except:

        font = None


    draw.multiline_text(
        (80, 700),
        text,
        fill=(255,255,255),
        font=font,
        spacing=20
    )


    image.save(
        output_path
    )


    print(
        "Fallback image saved:",
        output_path
    )


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
        prompt[:40]
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )


    image_path = os.path.join(
        output_folder,
        f"{filename}.png"
    )


    if os.path.exists(image_path):

        print(
            f"Using cached image: {image_path}"
        )

        return image_path



    print("=" * 60)
    print("GENERATING AI IMAGE")
    print("=" * 60)


    headers = {

        "Authorization":
        f"Bearer {HF_API_TOKEN}"

    }


    payload = {

        "inputs": prompt

    }


    try:

        response = requests.post(

            HF_IMAGE_API,

            headers=headers,

            json=payload,

            timeout=300

        )


        response.raise_for_status()


        content_type = response.headers.get(
            "content-type",
            ""
        )


        if "image" not in content_type:

            raise Exception(
                "HuggingFace did not return image data"
            )


        with open(
            image_path,
            "wb"
        ) as file:

            file.write(
                response.content
            )


        print(
            "AI image saved:",
            image_path
        )


        return image_path



    except Exception as e:


        print("=" * 60)
        print("HUGGINGFACE FAILED")
        print(e)
        print("=" * 60)


        # Never return None
        # Renderer always receives an image

        return create_fallback_image(
            prompt,
            image_path
    )
