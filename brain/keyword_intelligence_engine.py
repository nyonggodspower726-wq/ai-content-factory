from pytrends.request import TrendReq

pytrends = TrendReq(hl="en-US", tz=0)


KEYWORDS = [

    "ChatGPT prompts",

    "AI prompts",

    "Prompt engineering",

    "AI automation",

    "ChatGPT for business",

    "Prompt templates"

]


def get_keyword_opportunities():

    print("=" * 60)
    print("KEYWORD INTELLIGENCE ENGINE")
    print("=" * 60)

    opportunities = []

    for keyword in KEYWORDS:

        try:

            pytrends.build_payload(
                [keyword],
                timeframe="today 3-m"
            )

            related = pytrends.related_queries()

            if keyword in related:

                rising = related[keyword].get("rising")

                if rising is not None:

                    for item in rising["query"].tolist():

                        opportunities.append(item)

        except Exception as e:

            print(f"{keyword}: {e}")

    opportunities = list(dict.fromkeys(opportunities))

    print(f"Collected {len(opportunities)} keyword opportunities")

    if not opportunities:

        opportunities = [

            "Best ChatGPT prompts",

            "AI prompts for business",

            "Prompt engineering",

            "ChatGPT workflow",

            "AI productivity prompts",

            "Freelancer AI prompts"

        ]

    return opportunities
