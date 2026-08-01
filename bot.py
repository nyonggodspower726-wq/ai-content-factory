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

    log("Generating script...")
    script = generate_script(project)

    save_text("script.json", script)

    log("Generating voice...")
    voice = generate_voice(project)

    save_text("voice.json", voice)

    log("Generating SEO...")
    seo = generate_seo(topic)

    save_text("seo.json", seo)

    log("Generating AI scenes...")

    scenes = generate_scenes(
        project["scene_prompts"]
    )

    log("Rendering final video...")

    video = create_video(
        script,
        voice
    )

    if video:

        log("Uploading to TikTok...")
        upload_to_tiktok(video)

        log("Uploading to YouTube...")
        upload_to_youtube(
            video,
            seo,
            topic
        )

        log("Production Complete.")

    else:

        log("Video generation failed.")


if __name__ == "__main__":
    main()
