import requests
from bs4 import BeautifulSoup


PROMPT_MARKETPLACES = {

    "PromptBase": "https://promptbase.com",

    "FlowGPT": "https://flowgpt.com",

    "AIPRM": "https://www.aiprm.com"

}


def get_prompt_marketplace_trends():

    print("=" * 60)
    print("PROMPT MARKETPLACE ENGINE")
    print("=" * 60)

    trends = []

    headers = {

        "User-Agent": "PromptProHubBot/1.0"

    }

    for name, url in PROMPT_MARKETPLACES.items():

        try:

            response = requests.get(

                url,

                headers=headers,

                timeout=20

            )

            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )

            titles = soup.find_all(

                ["h1", "h2", "h3"]

            )

            for title in titles[:20]:

                text = title.get_text(strip=True)

                if len(text) > 10:

                    trends.append(text)

        except Exception as e:

            print(f"{name}: {e}")

    trends = list(dict.fromkeys(trends))

    print(f"Collected {len(trends)} prompt ideas")

    if not trends:

        trends = [

            "ChatGPT Business Prompts",

            "Freelancer Prompt Bundle",

            "Marketing Prompt Pack",

            "AI Automation Prompts",

            "Sales Prompt Templates",

            "Content Creator Prompt Pack",

            "SEO Prompt Collection",

            "Coding Prompt Library",

            "YouTube Prompt Bundle",

            "Prompt Engineering Toolkit"

        ]

    return trends
