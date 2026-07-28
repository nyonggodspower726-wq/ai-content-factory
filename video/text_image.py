from PIL import Image, ImageDraw, ImageFont

def create_title_image(text):

    width = 1080
    height = 1920

    image = Image.new("RGB", (width, height), (20, 20, 20))

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 70)
    except:
        font = ImageFont.load_default()

    draw.multiline_text(
        (80, 700),
        text,
        fill="white",
        font=font
    )

    image.save("title.png")

    return "title.png"
