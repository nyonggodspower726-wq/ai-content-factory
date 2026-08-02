from brain.production_manager import production

from brain.script_engine import generate_script
from brain.voice_engine import generate_voice
from brain.seo_engine import generate_seo

from video.ai_video_worker import generate_all_scenes
from video.video_generator import create_video

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log



def main(topic="Top 10 AI prompts for freelancers"):

    print("=" * 60)
    print("PromptProHub AI Studio Brain Online")
    print("=" * 60)

    print("=" * 60)
    print("AI CONTENT FACTORY v1.0")
    print("=" * 60)


    log(f"Starting campaign: {topic}")


    production_plan = production.produce(topic)


    project = production_plan["project"]


    log("Generating script...")


    script = generate_script(project)


    save_text(
        "script.json",
        script
    )


    log("Generating voice...")


    voice = generate_voice(project)


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


    log("Generating AI scenes...")


    scenes = generate_all_scenes(
        project["scene_prompts"]
    )


    if not scenes:

        log("No AI scenes generated")

        return



    log("Rendering final video...")


    video = create_video(
        script,
        voice
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
