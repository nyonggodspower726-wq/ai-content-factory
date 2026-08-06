import requests


PRODUCT_HUNT_API = "https://api.producthunt.com/v2/api/graphql"

ACCESS_TOKEN = "YOUR_PRODUCT_HUNT_ACCESS_TOKEN"


def get_producthunt_trends():

    print("=" * 60)
    print("PRODUCT HUNT ENGINE")
    print("=" * 60)

    query = """
    {
      posts(first:20){
        edges{
          node{
            name
            tagline
          }
        }
      }
    }
    """

    headers = {

        "Authorization": f"Bearer {ACCESS_TOKEN}",

        "Content-Type": "application/json"

    }

    trends = []

    try:

        response = requests.post(

            PRODUCT_HUNT_API,

            json={"query": query},

            headers=headers,

            timeout=20

        )

        data = response.json()

        posts = data["data"]["posts"]["edges"]

        for post in posts:

            title = post["node"]["name"]

            tagline = post["node"]["tagline"]

            trends.append(f"{title} - {tagline}")

    except Exception as e:

        print(e)

    trends = list(dict.fromkeys(trends))

    print(f"Collected {len(trends)} Product Hunt launches")

    if not trends:

        trends = [

            "New AI Prompt Generator",

            "ChatGPT Workflow Builder",

            "AI Prompt Marketplace",

            "AI Automation Tool"

        ]

    return trends
