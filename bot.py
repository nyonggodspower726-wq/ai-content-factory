from content.trend_finder import get_trending_topic
from content.script_writer import generate_script
from content.caption_writer import generate_caption
from content.hashtag_generator import generate_hashtags
from video.voice_generator import generate_voice
from video.video_generator import create_video
from social.tiktok_uploader import upload_to_tiktok


def main():

    print("=" * 50)
    print("AI CONTENT FACTORY")
    print("=" * 50)

    # Step 1
    topic = get_trending_topic()

    # Step 2
    script = generate_script(topic)

    # Step 3
    caption = generate_caption(topic)

    # Step 4
    hashtags = generate_hashtags()

    print(script)
    print(caption)
    print(hashtags)

    # Step 5
    generate_voice(script)

    # Step 6
    video = create_video()

    # Step 7
    if video:
        upload_to_tiktok(video)
    else:
        print("Video upload skipped.")

    print("Completed Successfully")


if __name__ == "__main__":
    main()
