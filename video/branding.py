import os

from PIL import Image, ImageDraw, ImageFont

from video.pexels_provider import generate_ai_image


class BrandingEngine:

    def __init__(self):

        self.brand_name = "PromptProHub"

        # =========================================
        # YOUTUBE THUMBNAIL SIZE — 16:9
        # =========================================

        self.width = 1280
        self.height = 720

        print("=" * 60)
        print("PROMPTPROHUB THUMBNAIL ENGINE READY")
        print("=" * 60)

    # =========================================
    # FONT
    # =========================================

    def get_font(self, size):

        possible_fonts = [

            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",

            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",

            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"

        ]

        for font_path in possible_fonts:

            if os.path.exists(font_path):

                return ImageFont.truetype(
                    font_path,
                    size
                )

        return ImageFont.load_default()

    # =========================================
    # PEXELS SEARCH
    # =========================================

    def build_image_search(self, hook):

        hook_lower = str(hook).lower()

        if "chatgpt" in hook_lower:

            return "man working laptop technology"

        if "prompt" in hook_lower:

            return "man working laptop office"

        if "ai" in hook_lower:

            return "man using artificial intelligence laptop"

        if "business" in hook_lower:

            return "business man laptop modern office"

        if "freelanc" in hook_lower:

            return "freelancer working laptop modern office"

        if "creator" in hook_lower:

            return "content creator laptop workspace"

        if "marketing" in hook_lower:

            return "digital marketer working laptop"

        if "sales" in hook_lower:

            return "business man computer office"

        return "man working laptop modern office"

    # =========================================
    # CREATE YOUTUBE THUMBNAIL
    # =========================================

    def create_hook_image(self, hook):

        print("=" * 60)
        print("CREATING YOUTUBE THUMBNAIL")
        print("=" * 60)

        search_query = self.build_image_search(
            hook
        )

        print(
            "Pexels search:",
            search_query
        )

        image_path = generate_ai_image(

            search_query,

            output_folder="assets/hook_images"

        )

        if not image_path:

            print(
                "Pexels thumbnail image failed."
            )

            return None

        if not os.path.exists(image_path):

            print(
                "Thumbnail image missing:",
                image_path
            )

            return None

        try:

            # =================================
            # OPEN IMAGE
            # =================================

            image = Image.open(
                image_path
            ).convert("RGB")

            # =================================
            # RESIZE TO COVER 1280x720
            # =================================

            source_width = image.width
            source_height = image.height

            scale = max(

                self.width / source_width,

                self.height / source_height

            )

            new_width = int(
                source_width * scale
            )

            new_height = int(
                source_height * scale
            )

            image = image.resize(
                (
                    new_width,
                    new_height
                ),
                Image.LANCZOS
            )

            # =================================
            # CENTER CROP
            # =================================

            left = (
                new_width -
                self.width
            ) // 2

            top = (
                new_height -
                self.height
            ) // 2

            image = image.crop(

                (
                    left,
                    top,

                    left +
                    self.width,

                    top +
                    self.height

                )

            )

            # =================================
            # DARK OVERLAY
            # =================================

            overlay = Image.new(

                "RGBA",

                image.size,

                (
                    0,
                    0,
                    0,
                    80
                )

            )

            image = Image.alpha_composite(

                image.convert("RGBA"),

                overlay

            )

            draw = ImageDraw.Draw(
                image
            )

            # =================================
            # FONTS
            # =================================

            hook_font = self.get_font(
                68
            )

            brand_font = self.get_font(
                30
            )

            # =================================
            # CLEAN HOOK
            # =================================

            hook = str(
                hook
            ).strip()

            if not hook:

                hook = (
                    "THIS CHANGES AI"
                )

            # =================================
            # LIMIT HOOK LENGTH
            # =================================

            words = hook.split()

            if len(words) > 8:

                words = words[:8]

                hook = " ".join(words)

            # =================================
            # WRAP HOOK
            # =================================

            lines = []

            current = ""

            for word in hook.split():

                test = (

                    current +
                    " " +
                    word

                ).strip()

                bbox = draw.textbbox(

                    (0, 0),

                    test,

                    font=hook_font

                )

                text_width = (

                    bbox[2] -
                    bbox[0]

                )

                if text_width <= 1050:

                    current = test

                else:

                    if current:

                        lines.append(
                            current
                        )

                    current = word

            if current:

                lines.append(
                    current
                )

            # Maximum 3 lines
            lines = lines[:3]

            # =================================
            # TEXT POSITION
            # =================================

            line_height = 82

            total_height = (

                len(lines) *
                line_height

            )

            start_y = (

                self.height // 2
                -
                total_height // 2

            )

            # =================================
            # DRAW HOOK
            # =================================

            for index, line in enumerate(
                lines
            ):

                bbox = draw.textbbox(

                    (0, 0),

                    line,

                    font=hook_font

                )

                text_width = (

                    bbox[2] -
                    bbox[0]

                )

                x = (

                    self.width -
                    text_width

                ) // 2

                y = (

                    start_y +
                    index *
                    line_height

                )

                # Shadow

                draw.text(

                    (
                        x + 5,
                        y + 5
                    ),

                    line,

                    font=hook_font,

                    fill=(

                        0,
                        0,
                        0,
                        220

                    )

                )

                # Main text

                draw.text(

                    (
                        x,
                        y
                    ),

                    line,

                    font=hook_font,

                    fill=(

                        255,
                        255,
                        255,
                        255

                    )

        )
