import os

from brain.production_manager import production
from brain.seo_engine import generate_seo

from video.video_generator import create_video

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log


def main(topic="Top 10 AI prompts for freelancers"):

    print("=" * 60)
    print("PROMPTPROHUB AI STUDIO ONLINE")
    print("=" * 60)

    try:

        log(
            f"Starting campaign: {topic}"
        )

        # =========================
        # BRAIN PRODUCTION
        # =========================

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

        print("Voice File :", voice_file)

        print(
            "Voice Exists :",
            bool(
                voice_file and os.path.exists(voice_file)
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

            log(
                "Uploading TikTok..."
            )

            upload_to_tiktok(
                video
            )

        except Exception as e:

            log(
                f"TikTok upload failed: {e}"
            )

        try:

            log(
                "Uploading YouTube Shorts..."
            )

            upload_to_youtube(

                video,

                seo,

                topic

            )

        except Exception as e:

            log(
                f"YouTube upload failed: {e}"
            )

        log(
            "Production completed successfully."
        )

    except Exception as e:

        log(
            f"BOT FAILED: {e}"
        )


if __name__ == "__main__":

    main()
