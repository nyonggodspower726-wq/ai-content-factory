import random

# Temporary topic pool
# Later this will be replaced with live trending topics.

TOPICS = [

    "AI tools replacing expensive software",

    "Hidden ChatGPT tricks nobody uses",

    "Best AI side hustles in 2026",

    "Freelancer mistakes costing thousands",

    "Passive income with AI",

    "AI business ideas with zero investment",

    "Best free AI websites",

    "How beginners make money online",

    "AI prompts that save hours",

    "Future jobs AI cannot replace",

    "Psychology tricks that increase sales",

    "Digital products that sell every day",

    "Marketing secrets brands use",

    "The biggest online business mistakes",

    "How creators grow without showing their face"

]


def choose_topic(memory=None):

    print("=" * 60)
    print("TOPIC DIVERSITY ENGINE")
    print("=" * 60)

    if memory is None:
        memory = []

    available = [

        topic

        for topic in TOPICS

        if topic not in memory

    ]

    if len(available) == 0:

        available = TOPICS.copy()

    topic = random.choice(available)

    print("Selected Topic:")

    print(topic)

    return topic
