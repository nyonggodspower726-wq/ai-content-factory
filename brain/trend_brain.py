from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are PromptProHub Demand Intelligence Engine.

Your job is to discover HIGH-DEMAND content opportunities
specifically for the PromptProHub business.

PromptProHub focuses on:

CORE NICHE:
- AI prompts
- ChatGPT prompts
- Prompt templates
- AI prompt engineering
- AI workflows
- AI productivity
- AI automation
- AI tools

DIGITAL PRODUCTS:
- AI prompt ebooks
- Prompt bundles
- ChatGPT guides
- AI templates
- AI business templates
- AI freelancer templates
- AI creator templates
- AI marketing templates
- AI productivity templates

TARGET AUDIENCE:
- Freelancers
- Business owners
- Content creators
- Digital marketers
- Entrepreneurs
- Students
- Professionals
- People trying to use AI to save time or make money

IMPORTANT:

Do NOT search for random global trends.

Do NOT generate topics about:
- Cryptocurrency
- Bitcoin
- Forex
- Sports
- Politics
- Celebrity news
- Entertainment
- Gaming
- General technology unrelated to AI prompts
- Random news

A topic is only acceptable if it has a strong connection
to AI prompts, ChatGPT, AI templates, AI workflows,
AI productivity, AI business use or AI digital products.

Your job is to identify topics with:

1. High current demand
2. Strong audience pain
3. Strong curiosity
4. Strong practical value
5. Strong commercial intent
6. Potential to lead naturally to an AI prompt/template/ebook

Prioritize problems people are actively trying to solve.

Examples:

"ChatGPT prompts for freelancers"

"AI prompts for writing better sales emails"

"ChatGPT prompts that save business owners hours"

"AI prompts for social media content"

"Best prompts for creating marketing campaigns"

"ChatGPT prompts for generating business ideas"

"AI prompt templates for content creators"

"AI prompts for customer service"

"ChatGPT prompts for freelancers who want more clients"

"AI prompts for creating digital products"

Do not simply repeat these examples.

Find fresh opportunities.

For each topic, think about:
- What problem is the person trying to solve?
- Why would they search for this?
- Could a useful prompt/template solve it?
- Could this eventually lead to a PromptProHub product?

Return ONLY valid JSON.

Format:

{
    "topics": [
        {
            "topic": "specific topic",
            "demand": 90,
            "pain": 85,
            "commercial_intent": 88,
            "content_potential": 92,
            "reason": "short explanation"
        }
    ]
}

Generate 20 opportunities.
"""


def discover_trending_topics():

    prompt = f"""
{SYSTEM_PROMPT}

Find 20 HIGH-DEMAND opportunities right now.

Focus specifically on people looking for:
AI prompts,
ChatGPT prompts,
prompt templates,
AI workflows,
AI productivity,
AI automation,
AI business solutions,
AI creator solutions,
AI freelancer solutions,
AI marketing solutions,
AI ebooks and guides.

Do not generate generic AI news.

Do not generate cryptocurrency topics.

Rank opportunities using demand, pain,
commercial intent and content potential.
"""

    try:

        response = ask_ai(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(response)

        opportunities = data.get(
            "topics",
            []
        )

        if not opportunities:
            raise Exception(
                "No trend opportunities returned"
            )

        # =========================
        # NICHE FILTER
        # =========================

        allowed_keywords = [
            "ai",
            "artificial intelligence",
            "chatgpt",
            "prompt",
            "prompts",
            "template",
            "templates",
            "automation",
            "workflow",
            "productivity",
            "digital product",
            "ebook",
            "marketing",
            "freelancer",
            "creator",
            "business"
        ]

        filtered = []

        for item in opportunities:

            if isinstance(item, dict):

                topic = item.get(
                    "topic",
                    ""
                )

            else:

                topic = str(item)

            topic_lower = topic.lower()

            if any(
                keyword in topic_lower
                for keyword in allowed_keywords
            ):

                filtered.append(item)

        if not filtered:

            raise Exception(
                "No relevant PromptProHub topics found"
            )

        print("=" * 60)
        print("PROMPTPROHUB DEMAND INTELLIGENCE")
        print("=" * 60)

        print(
            f"Generated opportunities: {len(opportunities)}"
        )

        print(
            f"Niche opportunities: {len(filtered)}"
        )

        print("=" * 60)

        return filtered

    except Exception as e:

        print(
            "Trend discovery failed:",
            e
        )

    # =========================
    # SAFE FALLBACK
    # =========================

    print("=" * 60)
    print("USING PROMPTPROHUB TREND FALLBACK")
    print("=" * 60)

    return [

        {
            "topic":
            "ChatGPT prompts that save freelancers hours every week",
            "demand": 90,
            "pain": 90,
            "commercial_intent": 88,
            "content_potential": 92
        },

        {
            "topic":
            "AI prompts for creating better social media content",
            "demand": 88,
            "pain": 84,
            "commercial_intent": 86,
            "content_potential": 92
        },

        {
            "topic":
            "AI prompt templates for small business owners",
            "demand": 87,
            "pain": 89,
            "commercial_intent": 94,
            "content_potential": 90
        },

        {
            "topic":
            "ChatGPT prompts for getting more freelance clients",
            "demand": 91,
            "pain": 92,
            "commercial_intent": 94,
            "content_potential": 95
        },

        {
            "topic":
            "AI prompts for creating digital products faster",
            "demand": 86,
            "pain": 88,
            "commercial_intent": 95,
            "content_potential": 93
        }

    ]


def choose_trending_topic():

    opportunities = discover_trending_topics()

    # =========================
    # SCORE OPPORTUNITIES
    # =========================

    scored = []

    for item in opportunities:

        if isinstance(item, dict):

            topic = item.get(
                "topic",
                ""
            )

            demand = float(
                item.get(
                    "demand",
                    0
                )
            )

            pain = float(
                item.get(
                    "pain",
                    0
                )
            )

            commercial = float(
                item.get(
                    "commercial_intent",
                    0
                )
            )

            content = float(
                item.get(
                    "content_potential",
                    0
                )
            )

            score = (

                demand * 0.30

                + pain * 0.20

                + commercial * 0.30

                + content * 0.20

            )

            scored.append(
                (
                    score,
                    topic
                )
            )

        else:

            scored.append(
                (
                    50,
                    str(item)
                )
            )

    if not scored:

        return (
            "ChatGPT prompts that save freelancers "
            "hours every week"
        )

    # Highest opportunity first

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    score, topic = scored[0]

    print("=" * 60)
    print("SELECTED HIGH-DEMAND TOPIC")
    print("=" * 60)

    print(
        f"Demand Score: {score:.1f}/100"
    )

    print(
        f"Topic: {topic}"
    )

    print("=" * 60)

    return topic
