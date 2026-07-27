from moviepy.editor import TextClip, CompositeVideoClip
from config import WEBSITE_URL, BRAND_NAME

def add_branding(video):

    website = TextClip(
        WEBSITE_URL,
        fontsize=40,
        color="white"
    ).set_duration(video.duration)

    website = website.set_position(("center", "bottom"))

    brand = TextClip(
        BRAND_NAME,
        fontsize=30,
        color="yellow"
    ).set_duration(video.duration)

    brand = brand.set_position(("left", "top"))

    final = CompositeVideoClip([
        video,
        website,
        brand
    ])

    return final
