from ai import ask_ai
from config import BRAND_NAME


def generate_script(topic):

    prompt = f"""
You are a world-class viral short-form copywriter.

Write ONE 30-45 second script for TikTok, YouTube Shorts,
Instagram Reels and Facebook Reels.

Topic:
{topic}

========================
HOOK REQUIREMENTS
========================

The first sentence MUST immediately grab attention.

NEVER start with:

"What if you could..."
"Imagine..."
"Imagine having..."
"Have you ever wondered..."
"Did you know..."
"In today's world..."
"Here are..."
"Let me tell you..."

Do NOT use generic motivational openings.

Use a direct, specific and curiosity-driven hook.

Preferred hook styles include:

"Watch me turn 10 hours of work into minutes."

"I tested this AI workflow and it completely changed how I work."

"I used this AI system to finish a task that normally takes all day."

"I found a way to do this in minutes instead of hours."

"Most people are doing this the hard way."

"This simple AI workflow can replace hours of repetitive work."

"I made [specific result] using AI, and here's exactly how."

"I tested [specific method] so you don't have to."

"If you're still doing this manually, you're wasting time."

"Here's the AI workflow I wish I discovered earlier."

IMPORTANT:

Do not invent fake achievements, income, sales,
results or personal experiences.

For example, NEVER claim:

"I made $100,000"

unless the topic/storyboard actually provides evidence
that this happened.

Instead, use a truthful version such as:

"Here's how this AI workflow can help you build
a system capable of generating more sales."

The hook should match the actual topic.

========================
STORY STRUCTURE
========================

Use this structure:

1. HARD HOOK
2. PROBLEM
3. DISCOVERY / INSIGHT
4. PRACTICAL SOLUTION
5. BENEFIT
6. STRONG CTA

Keep the pacing fast.

Every sentence should move the story forward.

Avoid unnecessary introductions.

Avoid repeating the same idea.

Use very simple English.

Sound like a real person speaking.

========================
BRAND
========================

Mention {BRAND_NAME} naturally when appropriate.

Do not force the brand name into every script.

========================
CTA
========================

The CTA MUST be the FINAL spoken words.

Do not place anything after the CTA.

Do not end the script before the CTA.

The CTA must be:

"Click the link in my bio to download premium AI prompt templates that save you hours of work."

Make sure the CTA is written as a complete spoken sentence.

========================
LENGTH
========================

Target approximately 75-95 spoken words.

This is important because the final CTA must have enough
time to be spoken clearly.

Do not create an excessively long script.

========================
RULES
========================

- No emojis.
- No hashtags.
- No stage directions.
- No titles.
- No bullet points.
- No quotation marks around the script.
- Output ONLY the spoken script.
"""

    return ask_ai(prompt)
