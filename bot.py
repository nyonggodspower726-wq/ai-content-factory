from brain.production_manager import production

from brain.seo_engine import generate_seo

from video.video_generator import create_video

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log



def main():

    print("=" * 60)
    print("PROMPTPROHUB AI OPERATING SYSTEM")
    print("=" * 60)


    log("Starting AI Production...")


    # AI Brain creates the campaign automatically
    production_plan = production.produce()


    project = production_plan["project"]

    topic = production_plan["topic"]

    script = production_plan["script"]

    voice = production_plan["voice"]



    log(f"AI Topic Generated: {topic}")



    log("Saving script...")

    save_text(
        "script.json",
        script
    )



    log("Saving voice data...")

    save_text(
        "voice.json",
        voice
    )



    log("Generating SEO...")

    seo = generate_seo(topic)


    save_text(
        "seo.json",
        seo
    )



    log("Rendering final video...")

    video = create_video(
        project["scene_prompts"],
        script,
        voice
    )



    if video:


        log("Uploading to TikTok...")

        upload_to_tiktok(
            video
        )


        log("Uploading to YouTube Shorts...")

        upload_to_youtube(
            video,
            seo,
            topic
        )


        log("Production Complete Successfully.")



    else:

        log("Video generation failed.")



if __name__ == "__main__":

    main()
