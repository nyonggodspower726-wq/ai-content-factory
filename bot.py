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

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log


def main(topic=None):

    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)

    try:

        # =========================
        # NEW CREATIVE BRAIN
        # =========================

        log("ACTIVATING NEW CONTENT BRAIN...")

        log("Running Trend Intelligence Engine...")

        if topic is None:
            topic = choose_trending_topic()

        log(f"Selected Viral Topic: {topic}")

        # =========================
        # VIRAL ANGLE
        # =========================

        angle = choose_best_angle(topic)

        # =========================
        # CURIOSITY
        # =========================

        curiosity = choose_curiosity(topic)

        # =========================
        # HOOK
        # =========================

        hook = choose_hook(
            topic,
            angle,
            curiosity
        )

        # =========================
        # RETENTION
        # =========================

        retention = choose_retention(topic)

        # =========================
        # SAVE CREATIVE BRAIN
        # =========================

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

        # =========================
        # BRAIN PRODUCTION
        # =========================

        log(f"Starting campaign: {topic}")

        log("Running AI production brain...")

        production_plan = production.produce(topic)

        if not production_plan:

            log("Production brain returned nothing")

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

        # =========================
        # SAVE SCRIPT
        # =========================

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

        # =========================
        # SEO
        # =========================

        log("Generating SEO...")

        seo = generate_seo(topic)

        save_text(
            "seo.json",
            seo
        )

        # =========================
        # DEBUG
        # =========================

        print("=" * 60)
        print("DEBUG INFORMATION")
        print("=" * 60)

        scene_prompts = project.get(
            "scene_prompts",
            []
        )

        print(
            "Voice File :",
            voice_file
        )

        print(
            "Voice Exists :",
            bool(
                voice_file
                and os.path.exists(
                    voice_file
                )
            )
        )

        print(
            "Scene Prompts :",
            len(scene_prompts)
        )

        if scene_prompts:

            print(
                "First Scene :",
                scene_prompts[0]
            )

        if isinstance(script, dict):

            print(
                "Script Keys :",
                list(script.keys())
            )

        else:

            print(
                "Script Type :",
                type(script)
            )

        print("=" * 60)

        # =========================
        # VIDEO
        # =========================

        log("Rendering AI sales video...")

        video = create_video(
            scene_prompts,
            script,
            voice_file
        )

        if not video:

            log("Video generation failed.")

            return

        if not os.path.exists(video):

            log(
                f"Rendered video not found: {video}"
            )

            return

        print("=" * 60)
        print("VIDEO CREATED SUCCESSFULLY")
        print(video)
        print("=" * 60)

        # =========================
        # SOCIAL UPLOAD
        # =========================

        try:

            log("Uploading TikTok...")

            upload_to_tiktok(
                video
            )

            log(
                "TikTok upload completed."
            )

        except Exception as e:

            log(
                f"TikTok upload failed: {e}"
            )

            print(
                "TikTok upload traceback:"
            )

            traceback.print_exc()

        # =========================
        # YOUTUBE SHORTS
        # =========================

        try:

            log(
                "Uploading YouTube Shorts..."
            )

            # =========================
            # EXTRACT SEO DATA
            # =========================

            if isinstance(seo, dict):

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

            # =========================
            # THUMBNAIL PATH
            # =========================

            thumbnail_path = (
                "assets/hook_images/"
                "promptprohub_hook.jpg"
            )

            # =========================
            # CHECK THUMBNAIL
            # =========================

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

            # =========================
            # UPLOAD TO YOUTUBE
            # =========================

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

        # =========================
        # COMPLETE
        # =========================

        log(
            "Production completed successfully."
        )

        print("=" * 60)
        print("BOT COMPLETED SUCCESSFULLY")
        print("=" * 60)

    except Exception as e:

        # =========================
        # FULL BOT ERROR
        # =========================

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
            f"BOT FAILED: {type(e).__name__}: {e}"
        )

        # Important:
        # Tell scheduler/Railway that the run really failed.
        raise


# =========================
# START BOT
# =========================

if __name__ == "__main__":

    main()
