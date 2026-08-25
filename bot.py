import os
import traceback

from brain.production_manager import production
from brain.seo_engine import generate_seo
from brain.trend_brain import choose_trending_topic
from video.video_generator import create_video

from social.status200_publisher import publish_to_status200

from file_manager import save_text
from logger import log


def main(topic=None):

    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)

    try:

        # =====================================================
        # TOPIC
        # =====================================================

        if topic is None:

            log("Selecting trending topic...")

            topic = choose_trending_topic()

        log(
            f"Selected Viral Topic: {topic}"
        )

        # =====================================================
        # PRODUCTION
        # =====================================================

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

        # =====================================================
        # EXTRACT PRODUCTION DATA
        # =====================================================

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
        # SAVE PROJECT DATA
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
        # SCENE PROMPTS
        # =====================================================

        scene_prompts = project.get(
            "scene_prompts",
            []
        )

        if not scene_prompts:

            log(
                "No scene prompts available."
            )

            return None

        # =====================================================
        # VIDEO PREPARATION
        # =====================================================

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

        # =====================================================
        # VIDEO GENERATION
        # =====================================================

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
# =====================================================
        # CAPTION
        # =====================================================

        caption = topic

        if isinstance(
            script,
            dict
        ):

            caption = script.get(
                "hook",
                topic
            )

        # =====================================================
        # ZERNIO — ALL THREE PLATFORMS
        # =====================================================
        #
        # ONE publisher handles:
        #
        # Instagram
        # TikTok
        # YouTube
        #
        # Do NOT separately call:
        #
        # publish_to_instagram()
        # upload_to_youtube()
        #
        # The three-account Zernio publisher handles
        # everything.
        # =====================================================

        try:

            log(
                "Publishing video through Zernio..."
            )

            result = publish_to_status200(
                video,
                caption
            )

            print("=" * 60)
            print("ZERNIO PUBLISH RESULT")
            print("=" * 60)

            print(
                result
            )

            print("=" * 60)

            # -------------------------------------------------
            # REPORT RESULTS
            # -------------------------------------------------

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
                    "Zernio successful platforms:",
                    len(successful)
                )

                print(
                    "Zernio failed platforms:",
                    len(failed)
                )

                for item in successful:

                    print(
                        "SUCCESS:",
                        item.get(
                            "platform",
                            "unknown"
                        )
                    )

                for item in failed:

                    print(
                        "FAILED:",
                        item.get(
                            "platform",
                            "unknown"
                        ),
                        "→",
                        item.get(
                            "error",
                            "Unknown error"
                        )
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

        # =====================================================
        # COMPLETE
        # =====================================================

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

        print("=" * 60)
return {
            "success": True,
            "topic": topic,
            "video": video,
            "seo": seo
        }

    except Exception as e:

        print("=" * 60)
        print("BOT FAILED")
        print("=" * 60)

        print(
            "ERROR TYPE:",
            type(e).__name__
        )

        print(
            "ERROR:",
            repr(e)
        )

        print("=" * 60)

        traceback.print_exc()

        log(
            f"BOT FAILED: "
            f"{type(e).__name__}: {e}"
        )

        return None


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    main()
