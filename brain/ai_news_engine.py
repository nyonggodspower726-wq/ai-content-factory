import feedparser


AI_NEWS_FEEDS = [

    "https://openai.com/news/rss.xml",

    "https://blog.google/technology/ai/rss/",

    "https://www.anthropic.com/news/rss.xml",

    "https://huggingface.co/blog/feed.xml"

]


def get_ai_news():

    print("=" * 60)
    print("AI NEWS ENGINE")
    print("=" * 60)

    news = []

    for feed in AI_NEWS_FEEDS:

        try:

            rss = feedparser.parse(feed)

            for article in rss.entries[:10]:

                news.append(article.title)

        except Exception as e:

            print(e)

    # Remove duplicates
    news = list(dict.fromkeys(news))

    print(f"Collected {len(news)} AI news headlines")

    if len(news) == 0:

        news = [

            "Latest ChatGPT update",

            "OpenAI releases new AI model",

            "Google launches new Gemini feature",

            "Anthropic announces Claude improvements",

            "New AI prompt engineering techniques"

        ]

    return news
