from brain.ai_router import ask_ai


CTA = (
    "Click the link in my bio to download premium "
    "AI prompt templates that save you hours of work."
)


def generate_script(project, selected_cta=None):

    topic = project.get(
        "topic",
        ""
    )

    product = project.get(
        "product",
        {}
    )

    angle = project.get(
        "marketing",
        {}
    )

    if selected_cta:
        selected_cta = str(
            selected_cta
        ).strip()

    # =====================================
    # FORCE OUR SOCIAL CTA
    # =====================================

    final_cta = CTA

    prompt = f"""
You are PromptProHub's professional
short-form video scriptwriter.

Create ONE highly engaging 30-45 second
spoken script for:

TikTok
YouTube Shorts
Instagram Reels
Facebook Reels

================================
TOPIC
================================

{topic}

================================
PRODUCT
================================

{product}

================================
MARKETING INFORMATION
================================

{angle}

================================
HOOK
================================

Start immediately with a powerful,
specific, curiosity-driven hook.

NEVER start with:

"What if you could..."
"What if..."
"Imagine..."
"Imagine having..."
"Have you ever..."
"Did you know..."
"Today..."
"In this video..."
"Welcome..."
"Let's talk about..."

Avoid generic motivational openings.

The first sentence must make someone
want to keep watching.

Examples of the style:

"Watch me turn 10 hours of work into minutes."

"Most freelancers are using ChatGPT completely wrong."

"You're wasting hours doing this manually."

"I tested this AI workflow so you don't have to."

================================
STRUCTURE
================================

Use this structure:

1. HARD HOOK
2. PROBLEM
3. DISCOVERY
4. PRACTICAL SOLUTION
5. BENEFIT
6. CTA

Keep the pacing fast.

Use simple conversational English.

Every sentence must move the story forward.

================================
CTA
================================

The CTA is extremely important.

The FINAL spoken words of the script
MUST be EXACTLY:

{final_cta}

Nothing may appear after the CTA.

Do NOT modify the CTA.

Do NOT shorten it.

Do NOT put anything after it.

Do NOT create another ending.

The script must finish with:

{final_cta}

================================
LENGTH
================================

Target approximately 75-95 spoken words.

The CTA must have enough space to be spoken
clearly.

================================
RULES
================================

- No emojis.
- No hashtags.
- No stage directions.
- No titles.
- No bullet points.
- No quotation marks around the script.
- Do not invent fake income.
- Do not invent fake achievements.
- Do not claim results that were not provided.
- Output ONLY the spoken script.
"""

    try:

        script = ask_ai(prompt)

        if not script:

            raise Exception(
                "AI returned empty script"
            )

        script = str(
            script
        ).strip()

        # =====================================
        # REMOVE MARKDOWN
        # =====================================

        script = (
            script
            .replace("```", "")
            .strip()
        )

        # =====================================
        # REMOVE POSSIBLE OLD CTA
        # =====================================

        old_cta_phrases = [

            "Visit PromptProHub.com",
            "Visit promptprohub.com",
            "Explore PromptProHub.com",
            "Explore PromptProHub",
            "Visit PromptProHub",
            "Check out PromptProHub.com"
        ]

        for phrase in old_cta_phrases:

            if phrase in script:

                script = script.replace(
                    phrase,
                    ""
                ).strip()

        # =====================================
        # GUARANTEE CTA
        # =====================================

        if final_cta.lower() not in script.lower():

            script = (
                script.rstrip()
                + " "
                + final_cta
            )

        else:

            # Remove everything after the CTA
            position = script.lower().find(
                final_cta.lower()
            )

            script = script[
                :position
            ].rstrip()

            script = (
                script
                + " "
                + final_cta
            )

        # =====================================
        # DEBUG
        # =====================================

        print("=" * 60)
        print("SCRIPT ENGINE")
        print("=" * 60)

        print(
            "Topic:",
            topic
        )

        print(
            "CTA PRESENT:",
            final_cta.lower() in script.lower()
        )

        print(
            "FINAL SCRIPT:"
        )

        print(script)

        print("=" * 60)

        return script

    except Exception as e:

        print("=" * 60)
        print("SCRIPT ENGINE FAILED")
        print("=" * 60)

        print(e)

        print("=" * 60)

        # =====================================
        # SAFE FALLBACK
        # =====================================

        fallback = (
            f"You're probably using {topic} "
            f"the hard way. "
            f"Here's a simpler AI workflow "
            f"that can save you hours of repetitive work. "
            f"Instead of doing everything manually, "
            f"use the right prompts and let AI handle "
            f"the repetitive parts. "
            f"{final_cta}"
        )

        return fallback
