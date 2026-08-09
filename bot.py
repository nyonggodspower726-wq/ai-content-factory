import os
import traceback

from brain.production_manager import production
from brain.seo_engine import generate_seo

from brain.trend_brain import choose_trending_topic
from brain.viral_angle_engine import choose_best_angle
from brain.curiosity_engine import choose_curiosity
from brain.hook_engine import choose_hook
from brain.retention_engine import choose_retention

from video.video_generator import create_video

# STATUS 200:
# TikTok #1, TikTok #2, LinkedIn, Pinterest
from social.status200_publisher import publish_to_status200

# DIRECT INSTAGRAM REELS API
from social.instagram_uploader import upload_to_instagram

from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log


# ============================================================
# RAILWAY PUBLIC URL
# ============================================================

RAILWAY_PUBLIC_DOMAIN = os.getenv(
    "RAILWAY_PUBLIC_DOMAIN"
)

RAILWAY_PUBLIC_URL = os.getenv(
    "RAILWAY_PUBLIC_URL"
)


def get_public_video_url(video_path):

    if RAILWAY_PUBLIC_DOMAIN:

        base_url = RAILWAY_PUBLIC_DOMAIN.strip()

        if not base_url.startswith(
            ("http://", "https://")
        ):

            base_url = "https://" + base_url

    elif RAILWAY_PUBLIC_URL:

        base_url = RAILWAY_PUBLIC_URL.strip()

        if not base_url.startswith(
            ("http://", "https://")
        ):

            base_url = "https://" + base_url

    else:

        raise RuntimeError(
            "Railway public URL is not configured. "
            "Set RAILWAY_PUBLIC_DOMAIN or "
            "RAILWAY_PUBLIC_URL in Railway Variables."
        )

    base_url = base_url.rstrip("/")

    filename = os.path.basename(video_path)

    return f"{base_url}/videos/{filename}"


# ============================================================
# MAIN
# ============================================================

def main(topic=None):

    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)

    try:

        # =====================================================
        # CREATIVE BRAIN
        # =====================================================

        log("ACTIVATING NEW CONTENT BRAIN...")
        log("Running Trend Intelligence Engine...")

        if topic is None:

            topic = choose_trending_topic()

        log(
            f"Selected Viral Topic: {topic}"
        )

        angle = choose_best_angle(topic)

        curiosity = choose_curiosity(topic)

        hook = choose_hook(
            topic,
            angle,
            curiosity
        )

        retention = choose_retention(topic)

        save_text(
            "creative_brain.json",
            {
                "topic": topic,
                "angle": angle,
                "curiosity": curiosity,
                "hook": hook,
                "retention": retention
            }
        )

        log(f"Selected Topic: {topic}")
        log(f"Hook: {hook}")
        log(f"Curiosity: {curiosity}")
        log(f"Retention: {retention}")

        # =====================================================
        # PRODUCTION
        # =====================================================

        log(
            f"Starting campaign: {topic}"
        )

        log(
            "Running AI production brain..."
        )

        production_plan = production.produce(
            topic
        )

        if not production_plan:

            log(
                "Production brain returned nothing"
            )

            return

        project = production_plan.get(
            "project",
            {}
        )

        script = production_plan.get(
            "script",
            {}
        )

        voice_file = production_plan.get(
            "voice"
        )

        # =====================================================
        # SAVE SCRIPT
        # =====================================================

        save_text(
            "script.json",
            script
        )

        save_text(
            "voice.json",
            production_plan.get(
                "voice_profile",
                {}
            )
        )

        # =====================================================
        # SEO
        # =====================================================

        log(
            "Generating SEO..."
        )

        seo = generate_seo(
            topic
        )

        save_text(
            "seo.json",
            seo
        )

        # =====================================================
        # DEBUG
        # =====================================================

        print("=" * 60)
        print("DEBUG INFORMATION")
        print("=" * 60)

        scene_prompts = project.get(
            "scene_prompts",
            []
        )

        print(
            "Voice File:",
            voice_file
        )

        print(
            "Voice Exists:",
            bool(
                voice_file
                and os.path.exists(
                    voice_file
                )
            )
        )

        print(
            "Scene Prompts:",
            len(scene_prompts)
        )

        if scene_prompts:

            print(
                "First Scene:",
                scene_prompts[0]
            )

        if isinstance(
            script,
            dict
        ):

            print(
                "Script Keys:",
                list(
                    script.keys()
                )
            )

        else:

            print(
                "Script Type:",
                type(script)
            )

        print("=" * 60)

        # =====================================================
        # VIDEO GENERATION
        # =====================================================

        log(
            "Rendering AI sales video..."
        )

        video = create_video(
            scene_prompts,
            script,
            voice_file
        )

        if not video:

            log(
                "Video generation failed."
            )

            return

        if not os.path.exists(
            video
        ):

            log(
                f"Rendered video not found: {video}"
            )

            return

        print("=" * 60)
        print("VIDEO CREATED SUCCESSFULLY")
        print(video)
        print("=" * 60)

        caption = hook

        # =====================================================
        # CREATE PUBLIC VIDEO URL
        # =====================================================

        public_video_url = (
            get_public_video_url(
                video
            )
        )

        print("=" * 60)
        print("PUBLIC VIDEO URL")
        print(public_video_url)
        print("=" * 60)

        # =====================================================
        # STATUS 200
        #
        # Account 1 = TikTok
        # Account 2 = LinkedIn
        # Account 3 = TikTok 2
        # Account 4 = Pinterest
        #
        # status200_publisher.py already handles all four
        # sequentially and continues if one account fails.
        # =====================================================

        try:

            log(
                "Publishing to Status 200 accounts..."
            )

            status200_result = (
                publish_to_status200(
                    video,
                    caption
                )
            )

            print("=" * 60)
            print(
                "STATUS 200 MULTI-ACCOUNT RESULT"
            )
            print("=" * 60)

            print(
                status200_result
            )

            log(
                "Status 200 publishing finished."
            )

        except Exception as e:

            log(
                f"Status 200 publishing failed: {e}"
            )

            print(
                "Status 200 traceback:"
            )

            traceback.print_exc()

        # =====================================================
        # DIRECT INSTAGRAM REELS API
        # =====================================================

        try:

            log(
                "Publishing Instagram Reel..."
            )

            instagram_result = (
                upload_to_instagram(
                    public_video_url,
                    caption
                )
            )

            print("=" * 60)
            print(
                "INSTAGRAM REEL PUBLISH SUCCESS"
            )
            print("=" * 60)

            print(
                instagram_result
            )

            log(
                "Instagram Reel publishing completed."
            )

        except Exception as e:

            print("=" * 60)
            print(
                "INSTAGRAM REEL PUBLISH FAILED"
            )
            print("=" * 60)

            print(
                "Error:",
                e
            )

            print(
                "Instagram traceback:"
            )

            traceback.print_exc()

            log(
                f"Instagram publishing failed: {e}"
            )

        # =====================================================
        # YOUTUBE SHORTS
        # =====================================================

        try:

            log(
                "Uploading YouTube Shorts..."
            )

            if isinstance(
                seo,
                dict
            ):

                youtube_title = seo.get(
                    "click_title",
                    seo.get(
                        "title",
                        topic
                    )
                )

                youtube_description = seo.get(
                    "description",
                    ""
                )

            else:

                youtube_title = topic

                youtube_description = str(
                    seo
                )

            thumbnail_path = (
                "assets/hook_images/"
                "promptprohub_hook.jpg"
            )

            if os.path.exists(
                thumbnail_path
            ):

                log(
                    f"YouTube thumbnail found: "
                    f"{thumbnail_path}"
                )

            else:

                log(
                    "YouTube thumbnail not found."
                )

                thumbnail_path = None

            upload_to_youtube(
                video,
                youtube_title,
                youtube_description,
                thumbnail_path
            )

            log(
                "YouTube upload completed."
            )

        except Exception as e:

            log(
                f"YouTube upload failed: {e}"
            )

            print(
                "YouTube upload traceback:"
            )

            traceback.print_exc()

        # =====================================================
        # COMPLETE
        # =====================================================

        log(
            "Production completed successfully."
        )

        print("=" * 60)
        print(
            "BOT COMPLETED SUCCESSFULLY"
        )
        print("=" * 60)

    except Exception as e:

        # =====================================================
        # FULL BOT ERROR
        # =====================================================

        print("=" * 60)
        print("BOT FAILED")
        print("=" * 60)

        print(
            f"ERROR TYPE: {type(e).__name__}"
        )

        print(
            f"ERROR: {repr(e)}"
        )

        print("=" * 60)
        print("FULL TRACEBACK")
        print("=" * 60)

        traceback.print_exc()

        print("=" * 60)

        log(
            f"BOT FAILED: "
            f"{type(e).__name__}: {e}"
        )

        raise


# ============================================================
# START BOT
# ============================================================

if __name__ == "__main__":

    main()
