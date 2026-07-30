from content.trend_finder import get_trending_topic
from content.script_writer import generate_script
from content.caption_writer import generate_caption
from content.hashtag_generator import generate_hashtags

from video.voice_generator import generate_voice
from video.video_generator import create_video

from social.tiktok_uploader import upload_to_tiktok
from social.youtube_shorts import upload_to_youtube

from file_manager import save_text
from logger import log


def main():

    print("TEST RUN STARTED")

    log("=" * 50)
    log("AI CONTENT FACTORY")
    log("=" * 50)

    # Step 1
    topic = get_trending_topic()
    log(f"Topic: {topic}")

    # Step 2
    script = generate_script(topic)

    # Step 3
    caption = generate_caption(topic)

    # Step 4
    hashtags = generate_hashtags()

    # Step 5
    save_text("script.txt", script)
    save_text("caption.txt", caption)
    save_text("hashtags.txt", hashtags)

    log("Script generated.")
    log("Caption generated.")
    log("Hashtags generated.")

    # Step 6
    voice = generate_voice(script)

    # Step 7
    video = create_video(script, voice)

    # Step 8
    if video:

        log("Uploading to TikTok...")
        upload_to_tiktok(video)

        log("Uploading to YouTube Shorts...")
        upload_to_youtube(
            video,
            caption,
            hashtags
        )

    else:
        log("Video upload skipped.")

    log("AI Content Factory completed successfully.")


if __name__ == "__main__":
    main()
