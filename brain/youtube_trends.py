import requests
from bs4 import BeautifulSoup


AI_KEYWORDS = [

    "ChatGPT",

    "AI prompts",

    "Prompt engineering",

    "AI automation",

    "OpenAI",

    "Claude AI",

    "Gemini AI",

    "AI business",

    "Freelancer AI"

]


def get_youtube_trends():

    print("=" * 60)
    print("YOUTUBE TREND ENGINE")
    print("=" * 60)

    results = []


    try:

        for keyword in AI_KEYWORDS:


            url = (
                "https://www.youtube.com/results?search_query="
                + keyword.replace(" ", "+")
            )


            headers = {

                "User-Agent":
                "Mozilla/5.0"

            }


            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )


            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            text = soup.get_text(
                " "
            )


            # Extract useful titles around keyword
            words = text.split("\n")


            for item in words:

                item = item.strip()

                if (
                    len(item) > 20
                    and keyword.lower() not in item.lower()
                ):

                    results.append(item)



    except Exception as e:

        print(
            "YouTube Trend Error:",
            e
        )



    results = list(
        dict.fromkeys(results)
    )


    print(
        f"Collected {len(results)} YouTube trends"
    )


    if not results:

        results = [

            "ChatGPT prompts that save hours",

            "AI prompts for business",

            "Prompt engineering secrets",

            "AI automation workflows",

            "How creators use ChatGPT"

        ]


    return results
