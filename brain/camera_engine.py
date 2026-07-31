import random


CAMERA_MOVES = [

    "slow dolly in",

    "slow dolly out",

    "cinematic orbit shot",

    "slow pan left",

    "slow pan right",

    "smooth crane shot",

    "steady handheld",

    "slow zoom in",

    "slow zoom out",

    "tracking shot",

    "over the shoulder",

    "close-up",

    "wide establishing shot",

    "low angle",

    "high angle",

    "macro shot"

]


LIGHTING = [

    "golden hour lighting",

    "soft studio lighting",

    "cinematic blue lighting",

    "warm natural light",

    "luxury office lighting",

    "dramatic contrast lighting",

    "professional commercial lighting"

]


COLOR_GRADING = [

    "teal and orange",

    "warm cinematic",

    "premium luxury",

    "dark modern",

    "high contrast",

    "clean corporate"

]


def apply_camera(prompt):

    camera = random.choice(CAMERA_MOVES)

    light = random.choice(LIGHTING)

    color = random.choice(COLOR_GRADING)

    enhanced = (

        f"{prompt}, "

        f"{camera}, "

        f"{light}, "

        f"{color}, "

        f"8k, "

        f"ultra realistic, "

        f"cinematic commercial quality"

    )

    return enhanced
