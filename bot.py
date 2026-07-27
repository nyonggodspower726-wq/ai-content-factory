from content.trend_finder import get_trending_topic
from content.website_reader import get_website_content
from content.script_writer import generate_script
from content.caption_writer import generate_caption
from content.hashtag_generator import generate_hashtags


def main():

    print("=" * 50)
    print(" AI CONTENT FACTORY ")
    print("=" * 50)

    print("Reading website...")
    website = get_website_content()

    print("Finding topic...")
    topic = get_trending_topic()

    print("Writing script...")
    script = generate_script(topic)

    print("Generating caption...")
    caption = generate_caption(topic)

    print("Generating hashtags...")
    hashtags = generate_hashtags()

    print("\n====================")
    print("TOPIC")
    print("====================")
    print(topic)

    print("\n====================")
    print("SCRIPT")
    print("====================")
    print(script)

    print("\n====================")
    print("CAPTION")
    print("====================")
    print(caption)

    print("\n====================")
    print("HASHTAGS")
    print("====================")
    print(hashtags)


if __name__ == "__main__":
    main()
