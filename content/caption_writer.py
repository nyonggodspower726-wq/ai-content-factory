from brain.ai import ask_ai


def generate_caption(topic):

    prompt = f"""
Write one engaging TikTok caption for:

{topic}

Requirements:
- Short
- Catchy
- Encourage engagement
- No emojis
"""

    return ask_ai(prompt)
