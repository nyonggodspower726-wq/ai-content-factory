from brain.ai_router import ask_ai
import json
import random



SYSTEM_PROMPT = """
You are PromptProHub Trend Intelligence Engine.

Your job is to discover fresh viral content opportunities.

Think like:

• MrBeast
• Alex Hormozi
• Ali Abdaal
• Iman Gadzhi

Generate topics people would stop scrolling to watch.

Focus on:

- New trends
- AI breakthroughs
- Creator economy
- Online business
- Digital products
- Marketing
- Productivity
- Money opportunities
- Future technology

Avoid boring titles.

Never use:

Top 10...
Best...
Guide...
Tutorial...
Welcome...

Use curiosity patterns:

"I tested..."
"Nobody is talking about..."
"The truth about..."
"This changed..."
"Why everyone is..."
"I tried..."
"The mistake..."

Return ONLY valid JSON.

Format:

{
 "topics":[
    "topic one",
    "topic two",
    "topic three"
 ]
}
"""



def discover_trending_topics():


    prompt = f"""
{SYSTEM_PROMPT}

Find 20 viral topics right now.
"""


    try:

        response = ask_ai(prompt)


        response = (
            response
            .replace("```json","")
            .replace("```","")
            .strip()
        )


        data = json.loads(response)


        topics = data.get(
            "topics",
            []
        )


        if topics:


            print("=" * 60)
            print("TREND INTELLIGENCE ENGINE")
            print("=" * 60)
            print(
                f"Generated {len(topics)} fresh topics"
            )
            print("=" * 60)


            return topics



    except Exception as e:

        print(
            "Trend discovery failed:",
            e
        )



    print("=" * 60)
    print("Using trend fallback")
    print("=" * 60)



    return [

        "The AI tool replacing expensive software",

        "The hidden ChatGPT feature creators ignore",

        "How AI is changing online businesses",

        "The mistake killing freelancer growth",

        "The future of AI content creation",

        "Why creators are switching to AI automation"

    ]





def choose_trending_topic():


    topics = discover_trending_topics()


    topic = random.choice(
        topics
    )


    print("=" * 60)
    print("SELECTED VIRAL TOPIC")
    print("=" * 60)
    print(topic)
    print("=" * 60)


    return topic
