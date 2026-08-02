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


def main():

    print("=" * 60)
    print("PROMPTPROHUB AI OPERATING SYSTEM")
    print("=" * 60)


    topic = input("Enter campaign topic: ")


    log("Starting AI Production...")


    production_plan = production.produce(topic)


    project = production_plan["project"]


    log("Generating Script...")

    script = generate_script(project)

    save_text(
        "script.json",
        script
    )


    log("Generating Voice...")

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


    log("Generating AI Scenes...")


    scenes = generate_all_scenes(
        project["scene_prompts"]
    )


    save_text(
        "scenes.json",
        scenes
    )


    if not scenes:

        log("No AI scenes generated.")

        log("Video generation stopped.")

        return



    log("Rendering Final Video...")


    video = create_video(
        script,
        voice
    )


    if not video:

        log("Video rendering failed.")

        return



    log("Uploading to TikTok...")

    upload_to_tiktok(video)



    log("Uploading to YouTube Shorts...")

    upload_to_youtube(
        video,
        seo,
        topic
    )



    log("Production Complete Successfully.")



if __name__ == "__main__":

    main()
