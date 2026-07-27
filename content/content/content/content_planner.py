from content.website_reader import get_website_content
from content.trend_finder import get_trending_topic


def create_content_plan():
    """
    Creates a content plan for the next video.
    """

    website = get_website_content()
    topic = get_trending_topic()

    return {
        "topic": topic,
        "website": website
    }
