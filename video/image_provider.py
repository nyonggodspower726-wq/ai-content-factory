import os
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont


# ==========================================================
# PROMPTPROHUB POLLINATIONS IMAGE PROVIDER
# ==========================================================

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/"


def create_fallback_image(prompt, output_path):

    print("=" * 60)
    print("CREATING FALLBACK IMAGE")
    print("=" * 60)

    width = 1080
    height = 1920

    image = Image.new(
        "RGB",
        (width, height),
        (18, 18, 18)
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

    except Exception:

        font = ImageFont.load_default()

    draw.multiline_text(

        (80, 650),

        text,

        fill=(255, 255, 255),

        font=font,

        spacing=18

    )

    image.save(output_path)

    print("Fallback image saved.")

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

        .replace(":", "_")

    )

    image_path = os.path.join(

        output_folder,

        f"{filename}.png"

    )

    # -------------------------------
    # Cache
    # -------------------------------

    if os.path.exists(image_path):

        print(

            f"Using cached image: {image_path}"

        )

        return image_path

    print("=" * 60)
    print("GENERATING AI IMAGE")
    print("=" * 60)

    cinematic_prompt = (

        prompt +

        ", ultra realistic, masterpiece, cinematic lighting, "

        "professional photography, volumetric light, "

        "high detail, 8k, HDR, sharp focus, "

        "vertical composition"

    )

    url = (

        POLLINATIONS_URL +

        urllib.parse.quote(cinematic_prompt)

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

        print("=" * 60)
        print("POLLINATIONS SUCCESS")
        print("=" * 60)

        print(image_path)

        return image_path

    except Exception as e:

        print("=" * 60)
        print("POLLINATIONS FAILED")
        print("=" * 60)
        print(e)

        return create_fallback_image(

            prompt,

            image_path

    )
