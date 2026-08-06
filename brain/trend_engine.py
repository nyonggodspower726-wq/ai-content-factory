from brain.google_trends import get_google_trends
from brain.youtube_trends import get_youtube_trends
from brain.reddit_trends import get_reddit_trends
from brain.x_trends import get_x_trends


def discover_trends(topic=None):

    print("=" * 60)
    print("TREND INTELLIGENCE ENGINE")
    print("=" * 60)

    trends = []

    # -------------------------
    # Google Trends
    # -------------------------
    try:
        trends.extend(get_google_trends())
    except Exception as e:
        print("Google Trends:", e)

    # -------------------------
    # YouTube Trends
    # -------------------------
    try:
        trends.extend(get_youtube_trends())
    except Exception as e:
        print("YouTube Trends:", e)

    # -------------------------
    # Reddit Trends
    # -------------------------
    try:
        trends.extend(get_reddit_trends())
    except Exception as e:
        print("Reddit Trends:", e)

    # -------------------------
    # X (Twitter) Trends
    # -------------------------
    try:
        trends.extend(get_x_trends())
    except Exception as e:
        print("X Trends:", e)

    # Remove duplicates while preserving order
    trends = list(dict.fromkeys(trends))

    print(f"Collected {len(trends)} trend ideas")

    return trends
