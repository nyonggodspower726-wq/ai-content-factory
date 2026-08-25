import os
import traceback

from brain.production_manager import production
from brain.seo_engine import generate_seo
from brain.trend_brain import choose_trending_topic
from video.video_generator import create_video

from social.status200_publisher import publish_to_status200

from file_manager import save_text
from logger import log


# ============================================================
# PROMPTPROHUB AI STUDIO
# ============================================================
#
# FLOW:
#
# Trending topic
#       ↓
# Production manager
#       ↓
# Script + voice + scene prompts
#       ↓
# SEO
#       ↓
# Video generation
#       ↓
# Railway public video
#       ↓
# Zernio three-account publisher
#       ↓
# Instagram + TikTok + YouTube
#
# ============================================================


def main(topic=None):

    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)

    try:

        # ====================================================
        # TOPIC
        # ====================================================

        if topic is None:

            log(
                "Selecting trending topic..."
            )

            topic = choose_trending_topic()

        if not topic:

            log(
                "No topic was selected."
            )

            return None

        topic = str(topic).strip()

        log(
            f"Selected Viral Topic: {topic}"
        )

        # ====================================================
        # PRODUCTION
        # ====================================================

        log(
            f"Starting production: {topic}"
        )

        production_plan = production.produce(
            topic
        )

        if not production_plan:

            log(
                "Production manager returned nothing."
            )

            return None

        # ====================================================
        # EXTRACT PRODUCTION DATA
        # ====================================================

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

        # ====================================================
        # SAVE PROJECT DATA
        # ====================================================

        try:

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

        except Exception as e:

            log(
                f"Project data save warning: {e}"
            )

            traceback.print_exc()

        # ====================================================
        # SEO
        # ====================================================

        log(
            "Generating SEO..."
        )

        seo = generate_seo(
            topic
        )

        try:

            save_text(
                "seo.json",
                seo
            )

        except Exception as e:

            log(
                f"SEO save warning: {e}"
            )

        # ====================================================
        # SCENE PROMPTS
        # ====================================================

        scene_prompts = project.get(
            "scene_prompts",
            []
        )

        if not scene_prompts:

            log(
                "No scene prompts available."
            )

            return None

        # ====================================================
        # VIDEO PREPARATION DEBUG
        # ====================================================

        print("=" * 60)
        print("VIDEO PREPARATION")
        print("=" * 60)

        print(
            "Topic:",
            topic
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
            "Scene Count:",
            len(scene_prompts)
        )

        print("=" * 60)

        # ====================================================
        # VIDEO GENERATION
        # ====================================================

        log(
            "Generating video..."
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

            return None

        if not os.path.exists(video):

            log(
                f"Rendered video not found: {video}"
            )

            return None

        print("=" * 60)
        print("VIDEO CREATED SUCCESSFULLY")
        print(video)
        print("=" * 60)
        # ====================================================
        # CAPTION
        # ====================================================

        caption = topic

        if isinstance(
            script,
            dict
        ):

            caption = script.get(
                "hook",
                topic
            )

        if not caption:

            caption = topic

        caption = str(
            caption
        ).strip()

        # ====================================================
        # ZERNIO THREE-ACCOUNT PUBLISHER
        # ====================================================
        #
        # This single function handles:
        #
        # Instagram
        # TikTok
        # YouTube
        #
        # Each platform uses its own Zernio API key.
        #
        # The publisher also discovers/verifies the connected
        # account through:
        #
        # GET /accounts
        #
        # ====================================================

        try:

            log(
                "Publishing video through Zernio..."
            )

            result = publish_to_status200(
                video,
                caption
            )

            print("=" * 60)
            print("ZERNIO PUBLISHING RESULT")
            print("=" * 60)

            print(
                result
            )

            print("=" * 60)

            # ----------------------------------------------
            # DISPLAY SUMMARY
            # ----------------------------------------------

            if isinstance(
                result,
                dict
            ):

                successful = result.get(
                    "successful",
                    []
                )

                failed = result.get(
                    "failed",
                    []
                )

                print(
                    "Successful platforms:",
                    len(successful)
                )

                print(
                    "Failed platforms:",
                    len(failed)
                )

                for item in successful:

                    if isinstance(
                        item,
                        dict
                    ):

                        print(
                            "SUCCESS:",
                            item.get(
                                "platform"
                            )
                        )

                for item in failed:

                    if isinstance(
                        item,
                        dict
                    ):

                        print(
                            "FAILED:",
                            item.get(
                                "platform"
                            ),
                            "→",
                            item.get(
                                "error"
                            )
                        )

            log(
                "Zernio publishing process completed."
            )

        except Exception as e:

            log(
                f"Zernio publishing failed: {e}"
            )

            print("=" * 60)
            print("ZERNIO PUBLISHING FAILED")
            print("=" * 60)

            print(
                "ERROR TYPE:",
                type(e).__name__
            )

            print(
                "ERROR:",
                str(e)
            )

            print("=" * 60)

            traceback.print_exc()

        # ====================================================
        # COMPLETE
        # ====================================================

        print("=" * 60)
        print("PROMPTPROHUB AI STUDIO COMPLETED")
        print("=" * 60)

        print(
            "Topic:",
            topic
        )

        print(
            "Video:",
            video
        )

        print(
            "Social publishing attempted:"
            " Instagram + TikTok + YouTube"
        )

        print("=" * 60)

        return {
            "success": True,
            "topic": topic,
            "video": video,
            "seo": seo
    }
