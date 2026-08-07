from pytrends.request import TrendReq
import time
import random


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


    pytrends = TrendReq(
        hl="en-US",
        tz=0,
        retries=2,
        backoff_factor=1
    )


    results = []


    for keyword in PROMPT_KEYWORDS:

        try:

            print(
                f"Searching: {keyword}"
            )


            pytrends.build_payload(
                [keyword],
                timeframe="now 7-d"
            )


            related = pytrends.related_queries()


            data = related.get(keyword)


            if data:

                top = data.get("top")


                if top is not None:

                    for value in top["query"].tolist():

                        results.append(value)



            # slow down requests
            time.sleep(
                random.randint(5,10)
            )


        except Exception as e:

            print(
                f"{keyword}: Google blocked request"
            )

            print(e)

            time.sleep(15)



    results = list(
        dict.fromkeys(results)
    )


    print(
        f"Collected {len(results)} Google trends"
    )


    if not results:

        print(
            "Using fallback trends"
        )


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
