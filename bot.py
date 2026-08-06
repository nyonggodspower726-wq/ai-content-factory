import os

from brain.production_manager import production
from brain.seo_engine import generate_seo

from brain.topic_engine import choose_topic
from brain.trend_brain import generate_trending_ideas
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

        log(
            "ACTIVATING NEW CONTENT BRAIN..."
        )


        if topic is None:

            topic = choose_topic()



        log(
            f"Generated Topic: {topic}"
        )



        # TREND BRAIN

        log(
            "Running Trend Brain..."
        )


        trend_ideas = generate_trending_ideas(
            topic
        )


        if trend_ideas:

            topic = trend_ideas[0]



        # VIRAL ANGLE

        angle = choose_best_angle(
            topic
        )



        # CURIOSITY

        curiosity = choose_curiosity(
            topic
        )



        # HOOK

        hook = choose_hook(
            topic,
            angle,
            curiosity
        )



        # RETENTION

        retention = choose_retention(
            topic
        )



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



        log(
            f"Selected Topic: {topic}"
        )

        log(
            f"Hook: {hook}"
        )

        log(
            f"Curiosity: {curiosity}"
        )

        log(
            f"Retention: {retention}"
        )



        # =========================
        # BRAIN PRODUCTION
        # =========================


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



        print(
            "Voice File :",
            voice_file
        )



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
