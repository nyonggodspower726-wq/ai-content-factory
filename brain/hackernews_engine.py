import requests


HACKER_NEWS_API = "https://hacker-news.firebaseio.com/v0"


def get_hackernews_trends():

    print("=" * 60)
    print("HACKER NEWS ENGINE")
    print("=" * 60)

    trends = []

    try:

        ids = requests.get(
            f"{HACKER_NEWS_API}/topstories.json",
            timeout=20
        ).json()

        for story_id in ids[:40]:

            story = requests.get(
                f"{HACKER_NEWS_API}/item/{story_id}.json",
                timeout=20
            ).json()

            if not story:
                continue

            title = story.get("title", "")

            keywords = [

                "AI",
                "ChatGPT",
                "OpenAI",
                "Claude",
                "Gemini",
                "Prompt",
                "LLM",
                "Agent",
                "Automation"

            ]

            if any(k.lower() in title.lower() for k in keywords):

                trends.append(title)

    except Exception as e:

        print(e)

    trends = list(dict.fromkeys(trends))

    print(f"Collected {len(trends)} Hacker News stories")

    if not trends:

        trends = [

            "New AI startup",

            "Latest ChatGPT feature",

            "Prompt engineering breakthrough",

            "AI agent framework",

            "Open-source AI tools"

        ]

    return trends
