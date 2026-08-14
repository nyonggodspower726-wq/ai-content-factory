import os
import traceback

from brain.production_manager import production
from brain.seo_engine import generate_seo
from brain.trend_brain import choose_trending_topic
from video.video_generator import create_video

from social.status200_publisher import publish_to_status200
from social.instagram_zernio import publish_to_instagram
from social.youtube_shorts import upload_to_youtube

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
        # DEBUG
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
        # STATUS 200
        # =====================================================

        try:

            log(
                "Publishing video through Status 200..."
            )

            result = publish_to_status200(
                video,
                caption
            )

            print(
                "Status 200 result:",
                result
            )

        except Exception as e:

            log(
                f"Status 200 publishing failed: {e}"
            )

            traceback.print_exc()

        # =====================================================
        # INSTAGRAM
        # =====================================================

        try:

            log(
                "Publishing Instagram Reel..."
            )

            result = publish_to_instagram(
                video,
                caption
            )

            print(
                "Instagram result:",
                result
            )

        except Exception as e:

            log(
                f"Instagram publishing failed: {e}"
            )

            traceback.print_exc()

        # =====================================================
        # YOUTUBE SHORT
        # =====================================================

        try:

            log(
                "Uploading YouTube Short..."
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

            if not os.path.exists(
                thumbnail_path
            ):

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


if __name__ == "__main__":

    main()
