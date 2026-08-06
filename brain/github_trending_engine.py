import requests
from bs4 import BeautifulSoup


GITHUB_TRENDING = "https://github.com/trending?since=daily"


def get_github_trends():

    print("=" * 60)
    print("GITHUB TRENDING ENGINE")
    print("=" * 60)

    trends = []

    try:

        response = requests.get(

            GITHUB_TRENDING,

            headers={
                "User-Agent": "PromptProHubBot/1.0"
            },

            timeout=20

        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        repos = soup.find_all(
            "h2",
            class_="h3 lh-condensed"
        )

        for repo in repos[:20]:

            name = repo.get_text(
                strip=True
            ).replace("\n", "")

            trends.append(name)

    except Exception as e:

        print(e)

    trends = list(dict.fromkeys(trends))

    print(f"Collected {len(trends)} GitHub repositories")

    if not trends:

        trends = [

            "OpenAI SDK",

            "LangChain",

            "CrewAI",

            "AutoGen",

            "Prompt Engineering Toolkit",

            "AI Agents"

        ]

    return trends
