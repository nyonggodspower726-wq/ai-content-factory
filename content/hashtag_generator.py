from ai import ask_ai


def generate_hashtags():

    prompt = """
Generate 15 trending TikTok hashtags for AI, business,
digital products, freelancing and online income.

Return only hashtags.
"""

    return ask_ai(prompt)
