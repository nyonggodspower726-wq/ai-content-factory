# content/script_writer.py

def generate_script(topic):
    """
    Generates a simple TikTok script.
    Later, this will use the OpenAI API to create high-quality scripts.
    """

    script = f"""
🎬 HOOK:
Did you know? {topic}

📖 BODY:
Here's why this matters and how it can help you.
Learn practical AI tips, save time, and improve your work with the right prompts.

📢 CALL TO ACTION:
Visit our website for premium AI prompts, eBooks, and templates.
"""

    return script
