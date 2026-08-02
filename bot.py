from brain.production_manager import production

from brain.seo_engine import generate_seo

from video.video_generator import create_video

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log



def main(topic="Top 10 AI prompts for freelancers"):


    print("=" * 60)
    print("PromptProHub AI Studio Brain Online")
    print("=" * 60)


    log(f"Starting campaign: {topic}")


    production_plan = production.produce(topic)


    project = production_plan["project"]

    script = production_plan["script"]

    voice_file = production_plan["voice"]


    save_text(
        "script.json",
        script
    )


    save_text(
        "voice.json",
        production_plan["voice_profile"]
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

        voice_file

    )


    if video:


        log("Uploading TikTok...")


        upload_to_tiktok(video)



        log("Uploading YouTube...")


        upload_to_youtube(

            video,

            seo,

            topic

        )


        log("Production Complete.")


    else:

        log("Video generation failed")



if __name__ == "__main__":

    main()
