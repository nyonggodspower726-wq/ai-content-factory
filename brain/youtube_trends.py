from brain.youtube_api import youtube


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

            response = youtube.search().list(

                q=keyword,

                part="snippet",

                maxResults=10,

                order="viewCount",

                type="video"

            ).execute()


            for item in response.get("items", []):

                title = item["snippet"]["title"]

                results.append(title)

    except Exception as e:

        print("YouTube API Error:", e)

    results = list(dict.fromkeys(results))

    print(f"Collected {len(results)} YouTube trends")

    if len(results) == 0:

        results = [

            "Best ChatGPT prompts",

            "AI prompts for business",

            "Prompt engineering tutorial",

            "ChatGPT automation",

            "AI workflow"

        ]

    return results
