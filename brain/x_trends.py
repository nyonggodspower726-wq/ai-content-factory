import feedparser


RSS_FEEDS = [

    "https://nitter.net/OpenAI/rss",

    "https://nitter.net/sama/rss",

    "https://nitter.net/GoogleAI/rss",

    "https://nitter.net/AnthropicAI/rss"

]


def get_x_trends():

    print("=" * 60)
    print("X TREND ENGINE")
    print("=" * 60)

    results = []

    for feed in RSS_FEEDS:

        try:

            rss = feedparser.parse(feed)

            for post in rss.entries[:10]:

                results.append(post.title)

        except Exception as e:

            print(e)

    # Remove duplicates
    results = list(dict.fromkeys(results))

    print(f"Collected {len(results)} X trends")

    if len(results) == 0:

        results = [

            "Latest ChatGPT update",

            "OpenAI new features",

            "AI Agents",

            "Prompt Engineering",

            "ChatGPT Business"

        ]

    return results
