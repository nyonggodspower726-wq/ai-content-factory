import os
import requests

from config import HF_API_TOKEN


# ==========================================
# PROMPTPROHUB IMAGE PROVIDER
# ==========================================

HF_IMAGE_API = (
    "https://api-inference.huggingface.co/models/"
    "black-forest-labs/FLUX.1-dev"
)


def generate_ai_image(prompt, output_folder="assets/images"):

    os.makedirs(output_folder, exist_ok=True)

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

        print(f"Using cached image: {image_path}")

        return image_path

    print("=" * 60)
    print("GENERATING AI IMAGE")
    print("=" * 60)

    headers = {

        "Authorization": f"Bearer {HF_API_TOKEN}"

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

        with open(image_path, "wb") as file:

            file.write(response.content)

        print("Image saved:", image_path)

        return image_path

    except Exception as e:

        print("=" * 60)
        print("IMAGE GENERATION FAILED")
        print("=" * 60)
        print(e)

        return None
