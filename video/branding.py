import os
import textwrap

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoFileClip,
    ImageClip,
    concatenate_videoclips
)

from video.pexels_provider import generate_ai_image


class BrandingEngine:

    def __init__(self):

        self.brand_name = "PromptProHub"

        self.width = 720
        self.height = 1280

        print("=" * 60)
        print("BRANDING ENGINE READY")
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
    # CREATE PEXELS SEARCH
    # =========================================

    def build_image_search(self, hook):

        hook_lower = hook.lower()

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

        return "man working laptop modern office"

    # =========================================
    # CREATE OPENING IMAGE
    # =========================================

    def create_hook_image(
        self,
        hook
    ):

        print("=" * 60)
        print("CREATING VIRAL HOOK COVER")
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
                "Pexels hook image failed."
            )

            return None

        if not os.path.exists(image_path):

            print(
                "Hook image missing:",
                image_path
            )

            return None

        try:

            image = Image.open(
                image_path
            ).convert("RGB")

            # =================================
            # RESIZE TO 9:16
            # =================================

            target_ratio = (
                self.width /
                self.height
            )

            image_ratio = (
                image.width /
                image.height
            )

            if image_ratio > target_ratio:

                new_height = image.height

                new_width = int(
                    new_height *
                    target_ratio
                )

            else:

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
                (new_width - self.width) // 2
            )

            top = max(
                0,
                (new_height - self.height) // 2
            )

            image = image.crop(
                (
                    left,
                    top,
                    left + self.width,
                    top + self.height
                )
            )

            # =================================
            # DARK OVERLAY
            # =================================

            overlay = Image.new(
                "RGBA",
                image.size,
                (0, 0, 0, 70)
            )

            image = Image.alpha_composite(
                image.convert("RGBA"),
                overlay
            )

            draw = ImageDraw.Draw(
                image
            )

            # =================================
            # HOOK FONT
            # =================================

            hook_font = self.get_font(
                58
            )

            brand_font = self.get_font(
                28
            )

            # =================================
            # WRAP HOOK
            # =================================

            words = hook.split()

            lines = []
            current = ""

            for word in words:

                test = (
                    current + " " + word
                ).strip()

                bbox = draw.textbbox(
                    (0, 0),
                    test,
                    font=hook_font
                )

                if bbox[2] <= 620:

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

            # Limit to a reasonable number
            # of lines

            lines = lines[:5]

            # =================================
            # HOOK POSITION
            # =================================

            line_height = 72

            total_height = (
                len(lines) *
                line_height
            )

            start_y = (
                self.height // 2
                - total_height // 2
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
                        x + 4,
                        y + 4
                    ),
                    line,
                    font=hook_font,
                    fill=(0, 0, 0, 190)
                )

                # Main text

                draw.text(
                    (
                        x,
                        y
                    ),
                    line,
                    font=hook_font,
                    fill=(255, 255, 255, 255)
                )

            # =================================
            # BRAND
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
                    self.height - 90
                ),
                brand_text,
                font=brand_font,
                fill=(255, 255, 255, 230)
            )

            # =================================
            # SAVE
            # =================================

            output_path = (
                "assets/hook_images/"
                "promptprohub_hook.jpg"
            )

            image.convert(
                "RGB"
            ).save(
                output_path,
                quality=95
            )

            print(
                "Hook cover created:",
                output_path
            )

            return output_path

        except Exception as e:

            print("=" * 60)
            print("HOOK IMAGE CREATION FAILED")
            print("=" * 60)

            print(e)

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
        # FALLBACK HOOK
        # =====================================

        if not hook_text:

            hook_text = (
                "AI can save you hours "
                "of repetitive work."
            )

        hook_text = str(
            hook_text
        ).strip()

        print("=" * 60)
        print("PROMPTPROHUB BRANDING ENGINE")
        print("=" * 60)

        print(
            "Hook:",
            hook_text
        )

        # =====================================
        # CREATE HOOK IMAGE
        # =====================================

        hook_image = self.create_hook_image(
            hook_text
        )

        if not hook_image:

            print(
                "Could not create hook frame."
            )

            print(
                "Returning original video."
            )

            return video_path

        try:

            # =================================
            # OPEN VIDEO
            # =================================

            video = VideoFileClip(
                video_path
            )

            # =================================
            # HOOK FRAME
            # =================================

            hook_clip = (
                ImageClip(
                    hook_image
                )
                .set_duration(2.0)
                .resize(
                    (
                        self.width,
                        self.height
                    )
                )
            )

            # Match FPS

            hook_clip = hook_clip.set_fps(
                video.fps or 30
            )

            # =================================
            # COMBINE
            # =================================

            final_video = concatenate_videoclips(
                [
                    hook_clip,
                    video
                ],
                method="compose"
            )

            # =================================
            # OUTPUT
            # =================================

            output_path = (
                "output/"
                "promptprohub_final.mp4"
            )

            os.makedirs(
                "output",
                exist_ok=True
            )

            print(
                "Rendering branded video..."
            )

            final_video.write_videofile(

                output_path,

                codec="libx264",

                audio_codec="aac",

                fps=video.fps or 30,

                threads=2,

                preset="veryfast",

                logger=None

            )

            final_video.close()

            video.close()

            print("=" * 60)
            print("BRANDED VIDEO READY")
            print(output_path)
            print("=" * 60)

            return output_path

        except Exception as e:

            print("=" * 60)
            print("BRANDING ENGINE FAILED")
            print("=" * 60)

            print(e)

            return video_path
