from brain.ai_router import ask_ai
import json
import os
import re
import time
from difflib import SequenceMatcher

HISTORY_FILE = "data/cta_history.json"
CTA_COOLDOWN = 10
MAX_HISTORY = 200
SIMILARITY_THRESHOLD = 0.78
PATTERN_THRESHOLD = 0.88

SYSTEM_PROMPT = """
You are the PromptProHub ELITE CTA ENGINE.

Your ONLY job is to create high-converting spoken CTAs
for short-form videos distributed across TikTok,
Instagram Reels, YouTube Shorts and LinkedIn.

The CTA is the final conversion moment.

Your mission:
CREATE DESIRE
CREATE A CLEAR NEXT STEP
MAKE THE OFFER FEEL RELEVANT
MAKE THE ACTION FEEL EASY
AVOID SOUNDING LIKE A ROBOTIC AD

PromptProHub sells practical AI prompts, prompt templates,
AI guides and digital resources for:
- Creators
- Freelancers
- Business owners
- Marketers
- AI users

================================
CORE CTA REQUIREMENTS
================================

The CTA should normally contain:
1. A natural action to check/click the bio link.
2. A natural reason to follow for more.

However, DO NOT force the exact same sentence structure.

Examples:

"Get the full prompt library through the link in my bio,
and follow for more practical AI workflows."

"The complete PromptProHub system is in my bio.
Follow if you want more useful AI strategies."

"Want the full version? Check the link in my bio,
then follow for the next one."

"Take the shortcut from the link in my bio,
and follow for more AI ideas you can actually use."

Do not make every CTA say:
"Click the link in my bio and follow for more."

================================
CTA PSYCHOLOGY
================================

Rotate across these psychological archetypes:

1. DIRECT OFFER
2. BENEFIT
3. CURIOSITY
4. FOMO
5. URGENCY
6. EXCLUSIVE ACCESS
7. CHEAT-CODE ENERGY
8. PROBLEM-SOLUTION
9. CHALLENGE
10. IDENTITY
11. AUTHORITY
12. FUTURE PACING
13. DISCOVERY
14. SAVINGS/TIME
15. PRODUCTIVITY
16. MONEY/RESULT
17. TOOLKIT
18. RESOURCE
19. NEXT-STEP
20. SOFT SELL
21. HARD SELL
22. "GET THE FULL VERSION"
23. "DON'T MISS THE NEXT ONE"
24. "SAVE TIME"
25. "BUILD FASTER"
26. "WORK SMARTER"
27. "SEE THE FULL SYSTEM"
28. "GET THE TEMPLATES"
29. "GET THE PROMPT LIBRARY"
30. "JOIN THE JOURNEY"

Do not use the same archetype repeatedly.

================================
MONEY CTA RULE
================================

Money/result CTAs may be used when the video actually
supports the claim.

NEVER invent:
- earnings
- clients
- customers
- sales
- guaranteed income
- fake results
- fake scarcity

NEVER say:
"This made me $500"
unless the supplied video data actually proves that.

Instead use credible language such as:
"Get the prompts designed to help you build faster."
"Explore the full prompt library through the link in my bio."

================================
FOMO AND URGENCY RULE
================================

Do not invent fake deadlines.

NEVER claim:
"48 hours only"
"price goes up tomorrow"
"this gets deleted"
"limited spots"
unless the system provides real evidence that this is true.

Use honest urgency instead:

"Don't wait until you're stuck again."
"Get the full toolkit when you're ready."
"Save this workflow and grab the complete version in my bio."

================================
CHEAT-CODE ENERGY
================================

You may use playful phrases such as:
"shortcut"
"cheat code"
"unfair advantage"
"secret weapon"

But NEVER falsely claim:
illegal
banned
leaked
secret government
celebrity-only
patched
confidential

unless the supplied information proves it.

================================
CTA STYLE
================================

The CTA should feel like the natural conclusion
of the video.

Do not suddenly switch into loud sales language.

Prefer:
specific
short
spoken
confident
human
clear

Avoid:
"Dear viewer..."
"Please kindly..."
"Act now!!!"
"Don't miss this incredible opportunity!!!"
"Like and subscribe."
"Thanks for watching."

================================
TOPIC MATCHING
================================

Match the CTA to what the video actually demonstrated.

Examples:

Money topic:
"Want the full prompt toolkit? Check the link in my bio,
and follow for more ways to build with AI."

Productivity topic:
"Grab the full prompt library from the link in my bio,
and follow for more ways to work faster."

AI discovery:
"Explore the complete AI toolkit through the link in my bio,
and follow for the next workflow."

Prompt tutorial:
"Get the full collection of ready-to-use prompts in my bio,
and follow for more."

Business topic:
"If you're building with AI, the full resource is in my bio.
Follow for more practical strategies."

================================
DIVERSITY
================================

Generate exactly 15 CTAs.

The 15 CTAs must feel genuinely different.

Do NOT simply replace one word.

Vary:
- sentence length
- opening
- psychological trigger
- action wording
- benefit
- emotional tone
- position of the follow request
- position of the product reference

================================
LENGTH
================================

Target:
10-30 spoken words.

Keep it natural.

================================
SCORING
================================

Score every CTA from 1-100:

conversion_potential
relevance
clarity
curiosity
urgency
natural_sounding
novelty
credibility

Return ONLY valid JSON.

Format:

{
  "ctas": [
    {
      "cta": "Get the full prompt library through the link in my bio,
      and follow for more practical AI workflows.",
      "archetype": "resource",
      "conversion_potential": 94,
      "relevance": 96,
      "clarity": 95,
      "curiosity": 88,
      "urgency": 82,
      "natural_sounding": 95,
      "novelty": 91,
      "credibility": 99
    }
  ]
}
"""


def ensure_history_directory():
    directory = os.path.dirname(HISTORY_FILE)

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )


def load_cta_history():
    ensure_history_directory()

    if not os.path.exists(
        HISTORY_FILE
    ):
        return []

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(
                file
            )

        if not isinstance(
            data,
            list
        ):
            return []

        return data

    except Exception as e:
        print("=" * 60)
        print("CTA HISTORY LOAD ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)

        return []


def save_cta_history(history):
    ensure_history_directory()

    try:
        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history[-MAX_HISTORY:],
                file,
                indent=2,
                ensure_ascii=False
            )

    except Exception as e:
        print("=" * 60)
        print("CTA HISTORY SAVE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)


def normalize_text(text):
    text = str(
        text or ""
    ).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


def similarity_score(
    first,
    second
):
    first = normalize_text(
        first
    )

    second = normalize_text(
        second
    )

    if not first or not second:
        return 0.0

    return SequenceMatcher(
        None,
        first,
        second
    ).ratio()


def get_cta_pattern(cta):
    words = normalize_text(
        cta
    ).split()

    if not words:
        return ""

    return " ".join(
        words[:5]
    )


def get_recent_ctas(history):
    return [
        item.get(
            "cta",
            ""
        )
        for item in history[
            -CTA_COOLDOWN:
        ]
        if (
            isinstance(
                item,
                dict
            )
            and item.get("cta")
        )
    ]


def get_recent_archetypes(
    history
):
    return {
        str(
            item.get(
                "archetype",
                ""
            )
        ).lower()

        for item in history[
            -8:
        ]

        if isinstance(
            item,
            dict
        )
    }


def is_recent_duplicate(
    cta,
    recent_ctas
):
    for old_cta in recent_ctas:

        if (
            normalize_text(cta)
            == normalize_text(old_cta)
        ):
            return True

        if similarity_score(
            cta,
            old_cta
        ) >= SIMILARITY_THRESHOLD:
            return True

    return False


def same_cta_pattern(
    first,
    second
):
    first_words = normalize_text(
        first
    ).split()

    second_words = normalize_text(
        second
    ).split()

    if (
        len(first_words) < 3
        or len(second_words) < 3
    ):
        return False

    first_prefix = " ".join(
        first_words[:4]
    )

    second_prefix = " ".join(
        second_words[:4]
    )

    if first_prefix == second_prefix:
        return True

    first_stem = " ".join(
        first_words[:3]
    )

    second_stem = " ".join(
        second_words[:3]
    )

    return (
        similarity_score(
            first_stem,
            second_stem
        )
        >= PATTERN_THRESHOLD
    )


def has_recent_pattern_repeat(
    cta,
    recent_ctas
):
    return any(
        same_cta_pattern(
            cta,
            old_cta
        )
        for old_cta in recent_ctas
    )


def record_cta_usage(
    history,
    cta,
    score,
    archetype,
    topic
):
    history.append({
        "cta": cta,
        "score": round(
            float(score),
            2
        ),
        "archetype": archetype,
        "pattern": get_cta_pattern(
            cta
        ),
        "topic": topic,
        "timestamp": time.time()
    })

    save_cta_history(
        history
)
