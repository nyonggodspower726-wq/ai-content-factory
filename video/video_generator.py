from video.background_video import download_background
from video.text_image import create_title_image

def create_video(script):

    print("Creating AI video...")

    background = download_background()

    image = create_title_image(script[:180])

    print("Background:", background)
    print("Title:", image)

    return background
