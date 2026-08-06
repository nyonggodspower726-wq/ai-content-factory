from brain.google_trends import get_google_trends
from brain.youtube_trends import get_youtube_trends
from brain.reddit_trends import get_reddit_trends
from brain.x_trends import get_x_trends
from brain.ai_news_engine import get_ai_news
from brain.producthunt_engine import get_producthunt_trends
from brain.github_trending_engine import get_github_trends
from brain.hackernews_engine import get_hackernews_trends
from brain.prompt_marketplace_engine import get_prompt_marketplace_trends
from brain.keyword_intelligence_engine import get_keyword_opportunities


def discover_trends(topic=None):

    print("=" * 60)
    print("TREND INTELLIGENCE ENGINE")
    print("=" * 60)

    trends = []

    # =========================================
    # GOOGLE TRENDS
    # =========================================
    try:
        trends.extend(get_google_trends())
    except Exception as e:
        print("Google Trends:", e)

    # =========================================
    # YOUTUBE
    # =========================================
    try:
        trends.extend(get_youtube_trends())
    except Exception as e:
        print("YouTube Trends:", e)

    # =========================================
    # REDDIT
    # =========================================
    try:
        trends.extend(get_reddit_trends())
    except Exception as e:
        print("Reddit Trends:", e)

    # =========================================
    # X (TWITTER)
    # =========================================
    try:
        trends.extend(get_x_trends())
    except Exception as e:
        print("X Trends:", e)

    # =========================================
    # AI NEWS
    # =========================================
    try:
        trends.extend(get_ai_news())
    except Exception as e:
        print("AI News:", e)

    # =========================================
    # PRODUCT HUNT
    # =========================================
    try:
        trends.extend(get_producthunt_trends())
    except Exception as e:
        print("Product Hunt:", e)

    # =========================================
    # GITHUB
    # =========================================
    try:
        trends.extend(get_github_trends())
    except Exception as e:
        print("GitHub:", e)

    # =========================================
    # HACKER NEWS
    # =========================================
    try:
        trends.extend(get_hackernews_trends())
    except Exception as e:
        print("Hacker News:", e)

    # =========================================
    # PROMPT MARKETPLACE
    # =========================================
    try:
        trends.extend(get_prompt_marketplace_trends())
    except Exception as e:
        print("Prompt Marketplace:", e)

    # =========================================
    # KEYWORD INTELLIGENCE
    # =========================================
    try:
        trends.extend(get_keyword_opportunities())
    except Exception as e:
        print("Keyword Intelligence:", e)

    # =========================================
    # REMOVE DUPLICATES
    # =========================================
    trends = list(dict.fromkeys(trends))

    # =========================================
    # FILTER FOR PROMPTPROHUB NICHE
    # =========================================
    keywords = [

        "prompt",
        "chatgpt",
        "openai",
        "ai",
        "gpt",
        "automation",
        "business",
        "marketing",
        "productivity",
        "freelancer",
        "agent",
        "workflow"

    ]

    filtered = []

    for trend in trends:

        if any(word in trend.lower() for word in keywords):
            filtered.append(trend)

    if filtered:
        trends = filtered

    print("=" * 60)
    print(f"Collected {len(trends)} PromptProHub trend ideas")
    print("=" * 60)

    return trends
