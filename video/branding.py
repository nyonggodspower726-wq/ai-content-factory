import os

from PIL import Image, ImageDraw, ImageFont

from video.pexels_provider import generate_ai_image


class BrandingEngine:

    def __init__(self):

        self.brand_name = "PromptProHub"

        # =========================================
        # YOUTUBE THUMBNAIL SIZE
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

            return "artificial intelligence laptop technology"

        if "business" in hook_lower:

            return "business man laptop office"

        if "freelanc" in hook_lower:

            return "freelancer working laptop"

        if "creator" in hook_lower:

            return "content creator laptop workspace"

        if "marketing" in hook_lower:

            return "digital marketer laptop office"

        if "sales" in hook_lower:

            return "business man laptop computer"

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
            # TARGET 16:9
            # =================================

            target_ratio = (
                self.width /
                self.height
            )

            image_ratio = (
                image.width /
                image.height
            )


            # =================================
            # CROP IMAGE TO 16:9
            # =================================

            if image_ratio > target_ratio:

                # Image is too wide

                new_height = image.height

                new_width = int(
                    new_height *
                    target_ratio
                )

            else:

                # Image is too tall

                new_width = image.width

                new_height = int(
                    new_width /
                    target_ratio
                )


            image = image.resize(
                (
                    new_width,
                    new_height
                )
            )


            # =================================
            # CENTER CROP
            # =================================

            left = max(
                0,
                (
                    new_width -
                    self.width
                ) // 2
            )

            top = max(
                0,
                (
                    new_height -
                    self.height
                ) // 2
            )


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
                    85
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
                    "AI CAN SAVE YOU HOURS "
                    "OF WORK"
                )


            # =================================
            # WRAP HOOK
            # =================================

            words = hook.split()

            lines = []

            current = ""


            for word in words:

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


            # =================================
            # LIMIT TEXT LINES
            # =================================

            lines = lines[:4]


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
            # =================================
            # BRAND NAME
            # =================================

            brand_text = self.brand_name


            bbox = draw.textbbox(

                (0, 0),

                brand_text,

                font=brand_font

            )


            brand_width = (

                bbox[2] -
                bbox[0]

            )


            brand_x = (

                self.width -
                brand_width

            ) // 2


            draw.text(

                (
                    brand_x,
                    self.height - 55
                ),

                brand_text,

                font=brand_font,

                fill=(
                    255,
                    255,
                    255,
                    235
                )

            )


            # =================================
            # SAVE THUMBNAIL
            # =================================

            os.makedirs(

                "assets/hook_images",

                exist_ok=True

            )


            output_path = (

                "assets/hook_images/"
                "promptprohub_hook.jpg"

            )


            image.convert(
                "RGB"
            ).save(

                output_path,

                "JPEG",

                quality=95,

                optimize=True

            )


            print(
                "YouTube thumbnail created:",
                output_path
            )


            print(
                "Thumbnail size:",
                f"{self.width}x{self.height}"
            )


            print("=" * 60)

            return output_path


        except Exception as e:

            print("=" * 60)
            print("THUMBNAIL CREATION FAILED")
            print("=" * 60)

            print(
                type(e).__name__
            )

            print(
                str(e)
            )

            return None


    # =========================================
    # APPLY BRANDING
    # =========================================

    def apply(
        self,
        video_path,
        hook_text=None
    ):

        if not video_path:

            print(
                "No video received."
            )

            return None


        if not os.path.exists(
            video_path
        ):

            print(
                "Video not found:",
                video_path
            )

            return None


        # =====================================
        # HOOK FALLBACK
        # =====================================

        if not hook_text:

            hook_text = (

                "AI CAN SAVE YOU HOURS "
                "OF WORK"

            )


        hook_text = str(
            hook_text
        ).strip()


        print("=" * 60)
        print("PROMPTPROHUB THUMBNAIL ENGINE")
        print("=" * 60)


        print(
            "Hook:",
            hook_text
        )


        # =====================================
        # CREATE SEPARATE THUMBNAIL
        # =====================================

        thumbnail = self.create_hook_image(

            hook_text

        )


        if thumbnail:

            print(
                "Thumbnail ready:",
                thumbnail
            )

        else:

            print(
                "Thumbnail could not be created."
            )


        # =====================================
        # IMPORTANT
        # =====================================
        #
        # The video itself is NOT modified.
        #
        # No opening image.
        # No 2-second hook frame.
        # No concatenate_videoclips().
        # No second video render.
        #
        # The thumbnail is saved separately
        # for the YouTube uploader.
        # =====================================


        print("=" * 60)

        print(
            "VIDEO LEFT UNCHANGED"
        )

        print(
            "SEPARATE YOUTUBE THUMBNAIL READY"
        )

        print(
            "Thumbnail:",
            thumbnail
        )

        print("=" * 60)


        return video_path
