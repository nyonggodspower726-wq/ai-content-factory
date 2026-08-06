from pytrends.request import TrendReq

pytrends = TrendReq(hl="en-US", tz=0)


PROMPT_KEYWORDS = [

    "ChatGPT prompts",

    "AI prompts",

    "Prompt engineering",

    "ChatGPT for business",

    "ChatGPT for freelancers",

    "AI automation",

    "AI workflow",

    "Prompt templates",

    "AI productivity",

    "OpenAI"

]


def get_google_trends():

    print("=" * 60)
    print("GOOGLE TRENDS ENGINE")
    print("=" * 60)

    results = []

    for keyword in PROMPT_KEYWORDS:

        try:

            pytrends.build_payload(
                [keyword],
                timeframe="now 7-d"
            )

            related = pytrends.related_queries()

            if keyword in related:

                top = related[keyword].get("top")

                if top is not None:

                    for value in top["query"].tolist():

                        results.append(value)

        except Exception as e:

            print(f"{keyword}: {e}")

    # Remove duplicates
    results = list(dict.fromkeys(results))

    print(f"Collected {len(results)} Google trends")

    if len(results) == 0:

        results = [

            "Best ChatGPT prompts",

            "AI prompts",

            "Prompt engineering",

            "ChatGPT workflow",

            "Prompt templates",

            "AI automation",

            "Freelancer AI",

            "Business AI",

            "OpenAI",

            "ChatGPT productivity"

        ]

    return results
