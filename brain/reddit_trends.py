import requests


SUBREDDITS = [

    "ChatGPT",

    "OpenAI",

    "PromptEngineering",

    "ArtificialIntelligence",

    "MachineLearning",

    "Entrepreneur",

    "Freelance"

]


HEADERS = {

    "User-Agent": "PromptProHubTrendBot/1.0"

}


def get_reddit_trends():

    print("=" * 60)
    print("REDDIT TREND ENGINE")
    print("=" * 60)

    results = []

    for subreddit in SUBREDDITS:

        try:

            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"

            response = requests.get(

                url,

                headers=HEADERS,

                timeout=10

            )

            data = response.json()

            posts = data.get("data", {}).get("children", [])

            for post in posts:

                title = post["data"]["title"]

                results.append(title)

        except Exception as e:

            print(f"{subreddit}: {e}")

    # Remove duplicates
    results = list(dict.fromkeys(results))

    print(f"Collected {len(results)} Reddit trends")

    if len(results) == 0:

        results = [

            "Best ChatGPT prompts",

            "Prompt engineering tips",

            "AI automation",

            "Freelancer AI workflow",

            "ChatGPT business ideas"

        ]

    return results
