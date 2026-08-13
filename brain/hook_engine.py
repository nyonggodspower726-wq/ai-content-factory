from brain.ai_router import ask_ai
import json
import os
import re
import time
from difflib import SequenceMatcher

HISTORY_FILE = "data/hook_history.json"
HOOK_COOLDOWN = 20
MAX_HISTORY = 200
SIMILARITY_THRESHOLD = 0.78
PATTERN_THRESHOLD = 0.88

SYSTEM_PROMPT = """
You are the PromptProHub ELITE VIRAL HOOK ENGINE.

Your job is to create extremely strong short-form hooks for
TikTok, Instagram Reels, YouTube Shorts, LinkedIn and other
short-form social platforms.

The hook is the FIRST thing the viewer hears and sees.

Your mission:
STOP THE SCROLL
CREATE AN INFORMATION GAP
CREATE EMOTIONAL TENSION
PROMISE A SPECIFIC PAYOFF
MAKE SCROLLING AWAY FEEL LIKE MISSING SOMETHING

PromptProHub focuses on:
- AI prompts
- ChatGPT
- prompt engineering
- AI productivity
- AI automation
- AI workflows
- AI tools
- AI for creators
- AI for freelancers
- AI for marketers
- AI for businesses
- AI digital products
- AI templates
- AI guides
- AI systems

================================
2026 HOOK PSYCHOLOGY
================================

Prioritize high-stakes ideas when they truthfully fit the topic:

MONEY
TIME
COMPETITIVE ADVANTAGE
AI DISRUPTION
CAREER PRESSURE
CURIOSITY
SURPRISE
CONTRAST
STATUS
EFFICIENCY
UNFAIR ADVANTAGE
MISTAKES
HIDDEN CAPABILITIES
BEFORE VS AFTER
EXPERIMENTS
CHALLENGES
SPECIFIC RESULTS

The hook should feel urgent, concrete and consequential.

Do NOT make every hook aggressive.
Use controlled variation so the audience does not feel manipulated.

================================
HOOK ARCHETYPES
================================

Generate hooks across DIFFERENT archetypes.

1. MONEY/RESULT
Example:
"This prompt can turn one rough idea into a client-ready offer."

2. AI DISRUPTION
Example:
"AI is changing this workflow faster than most businesses realize."

3. CONTRARIAN
Example:
"Buying another AI tool won't fix a bad prompt."

4. CHEAT-CODE ENERGY
Example:
"This feels like cheating, but it's just a better prompt."

5. CURIOSITY GAP
Example:
"I gave ChatGPT one sentence and this is what it produced."

6. MISTAKE
Example:
"Your ChatGPT results are weak because you're missing this."

7. WARNING
Example:
"Stop using ChatGPT this way if you're trying to save time."

8. BEFORE/AFTER
Example:
"One prompt took this from a blank page to a usable strategy."

9. EXPERIMENT
Example:
"I tested three prompts for the same task. Only one survived."

10. CHALLENGE
Example:
"Try this prompt before paying someone to do it manually."

11. SPECIFIC AUDIENCE
Example:
"If you're a freelancer, this prompt belongs in your workflow."

12. SPEED
Example:
"This takes seconds once you give AI the right instructions."

13. HIDDEN CAPABILITY
Example:
"Most people use ChatGPT for writing. It can do this too."

14. STATUS/ADVANTAGE
Example:
"The advantage isn't another AI tool. It's knowing what to ask."

15. SHOCK/CONTRAST
Example:
"Most people add more tools. Better operators fix the prompt."

================================
TRUTH AND CREDIBILITY RULE
================================

NEVER invent:
- earnings
- customers
- clients
- company names
- celebrity involvement
- leaked information
- secret partnerships
- bans
- lawsuits
- government claims
- statistics
- product capabilities
- personal experiences

NEVER claim:
"I made $10,000"
"Elon Musk uses this"
"OpenAI banned this"
"This is illegal"
"This prompt is leaked"
"90% of jobs will disappear"
unless the supplied topic or verified information explicitly proves it.

You may create urgency and high-stakes curiosity WITHOUT lying.

Allowed:
"This could replace hours of repetitive work."

Not allowed:
"This replaces three employees."

unless that claim is actually supported.

================================
FORBIDDEN OPENINGS
================================

NEVER start with:
"What if..."
"Imagine..."
"Have you ever..."
"Did you know..."
"Today..."
"In this video..."
"Welcome..."
"Let's talk about..."
"Here's..."
"Here are..."
"Let me show you..."
"Want to..."
"Do you want to..."
"Are you tired of..."

Avoid weak generic motivational language.

Avoid:
"This changes everything."
"This is amazing."
"You need to see this."
"Nobody is ready for this."

unless followed by a specific credible reason.

================================
ANTI-REPETITION
================================

Never generate 15 hooks that sound like one hook rewritten.

Avoid overusing:
"You're wasting..."
"Most people..."
"Stop..."
"I tested..."
"I found..."
"This..."
"The problem..."
"Don't..."

Use different sentence structures, emotional triggers
and opening words.

The hook must sound fresh even when the topic is similar.

================================
LENGTH
================================

Target:
8-18 spoken words.

Prefer short, punchy language.

Avoid long explanations.

Avoid unnecessary adjectives.

Every word should earn its place.

================================
PLATFORM NEUTRALITY
================================

Hooks must work naturally on:
TikTok
Instagram Reels
YouTube Shorts
LinkedIn

Do not use platform-specific slang unless it improves
the actual hook.

================================
SCORING
================================

Score every hook from 1-100:

scroll_stopping_power
curiosity
specificity
benefit
emotional_tension
credibility
natural_sounding
novelty

The best hook is NOT simply the loudest hook.

A strong hook must combine:
attention + curiosity + believable payoff.

Return ONLY valid JSON.

Format:
{
  "hooks": [
    {
      "hook": "I gave ChatGPT one sentence and watched it build the strategy.",
      "archetype": "curiosity_gap",
      "scroll_stopping_power": 94,
      "curiosity": 96,
      "specificity": 91,
      "benefit": 89,
      "emotional_tension": 88,
      "credibility": 98,
      "natural_sounding": 95,
      "novelty": 94
    }
  ]
}
"""

def ensure_history_directory():
    directory = os.path.dirname(HISTORY_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)

def load_hook_history():
    ensure_history_directory()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            return []
        return data
    except Exception as e:
        print("=" * 60)
        print("HOOK HISTORY LOAD ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)
        return []

def save_hook_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history[-MAX_HISTORY:], file, indent=2, ensure_ascii=False)
    except Exception as e:
        print("=" * 60)
        print("HOOK HISTORY SAVE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)

def normalize_text(text):
    text = str(text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def word_list(text):
    return normalize_text(text).split()

def similarity_score(first, second):
    first = normalize_text(first)
    second = normalize_text(second)
    if not first or not second:
        return 0.0
    return SequenceMatcher(None, first, second).ratio()

def get_hook_pattern(hook):
    words = word_list(hook)
    if not words:
        return ""
    return " ".join(words[:5])

def same_opening_pattern(first, second):
    first_words = word_list(first)
    second_words = word_list(second)
    if len(first_words) < 3 or len(second_words) < 3:
        return False
    first_prefix = " ".join(first_words[:4])
    second_prefix = " ".join(second_words[:4])
    if first_prefix == second_prefix:
        return True
    first_stem = " ".join(first_words[:3])
    second_stem = " ".join(second_words[:3])
    return similarity_score(first_stem, second_stem) >= PATTERN_THRESHOLD

def get_recent_hooks(history):
    return [
        item.get("hook", "")
        for item in history[-HOOK_COOLDOWN:]
        if isinstance(item, dict) and item.get("hook")
    ]

def is_recent_duplicate(hook, recent_hooks):
    for old_hook in recent_hooks:
        if normalize_text(hook) == normalize_text(old_hook):
            return True
        if similarity_score(hook, old_hook) >= SIMILARITY_THRESHOLD:
            return True
    return False

def has_recent_pattern_repeat(hook, recent_hooks):
    return any(
        same_opening_pattern(hook, old_hook)
        for old_hook in recent_hooks
    )

def record_hook_usage(history, hook, score, archetype):
    history.append({
        "hook": hook,
        "score": round(float(score), 2),
        "archetype": archetype,
        "pattern": get_hook_pattern(hook),
        "timestamp": time.time()
    })
    save_hook_history(history)
def generate_hooks(topic, angle, curiosity):
    history = load_hook_history()
    recent_hooks = get_recent_hooks(history)
    recent_examples = recent_hooks[-12:]
    recent_text = "\n".join(
        f"- {hook}"
        for hook in recent_examples
    )
    prompt = f"""
{SYSTEM_PROMPT}

================================
CURRENT TOPIC
================================
{topic}

================================
CURRENT VIRAL ANGLE
================================
{angle}

================================
CURRENT CURIOSITY
================================
{curiosity}

================================
RECENTLY USED HOOKS
================================
These hooks were recently used.

DO NOT copy them.
DO NOT lightly rewrite them.
DO NOT repeat their opening structure.
DO NOT reuse the same psychological angle.

{recent_text}

================================
BATCH DESIGN
================================
Generate exactly 15 candidates.

Use different archetypes across the batch.

Do not make the batch dominated by:
"You're..."
"Most..."
"Stop..."
"I..."
"This..."

Prioritize hooks that create a strong information gap.

When a money angle is appropriate, make the benefit concrete
without promising guaranteed income.

When an AI disruption angle is appropriate, create urgency
without inventing predictions or statistics.

When using "cheat-code" energy, make it metaphorical and
credible rather than falsely claiming something is illegal,
banned or leaked.

The viewer should immediately understand:
WHAT is at stake
WHY it matters
WHY they should keep watching.

Return ONLY valid JSON.
"""
    try:
        response = ask_ai(prompt)
        response = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(response)
        hooks = data.get("hooks", [])
        if not hooks:
            raise Exception("AI returned no hooks")
        cleaned_hooks = []
        for item in hooks:
            if not isinstance(item, dict):
                continue
            hook = str(item.get("hook", "")).strip()
            if not hook:
                continue
            try:
                scores = {
                    "scroll": float(item.get("scroll_stopping_power", 0)),
                    "curiosity": float(item.get("curiosity", 0)),
                    "specificity": float(item.get("specificity", 0)),
                    "benefit": float(item.get("benefit", 0)),
                    "emotion": float(item.get("emotional_tension", 0)),
                    "credibility": float(item.get("credibility", 0)),
                    "natural": float(item.get("natural_sounding", 0)),
                    "novelty": float(item.get("novelty", 0))
                }
            except (TypeError, ValueError):
                continue
            weighted_score = (
                scores["scroll"] * 0.22 +
                scores["curiosity"] * 0.18 +
                scores["specificity"] * 0.13 +
                scores["benefit"] * 0.13 +
                scores["emotion"] * 0.10 +
                scores["credibility"] * 0.10 +
                scores["natural"] * 0.07 +
                scores["novelty"] * 0.07
            )
            archetype = str(
                item.get(
                    "archetype",
                    "unknown"
                )
            ).strip().lower()
            cleaned_hooks.append({
                "score": weighted_score,
                "hook": hook,
                "archetype": archetype
            })
        if not cleaned_hooks:
            raise Exception("No valid hooks remained after parsing.")
        cleaned_hooks.sort(
            reverse=True,
            key=lambda item: item["score"]
        )
        print("=" * 60)
        print("ELITE VIRAL HOOK ENGINE")
        print("=" * 60)
        print(f"Generated: {len(cleaned_hooks)}")
        print(f"Recent hooks: {len(recent_hooks)}")
        print("=" * 60)
        return cleaned_hooks
    except Exception as e:
        print("=" * 60)
        print("HOOK ENGINE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)
        return [
            {
                "score": 95,
                "hook": f"Most people are using {topic} the wrong way.",
                "archetype": "contrarian"
            },
            {
                "score": 94,
                "hook": f"I found a faster way to handle {topic}.",
                "archetype": "result"
            },
            {
                "score": 93,
                "hook": f"This {topic} mistake can waste hours.",
                "archetype": "mistake"
            },
            {
                "score": 92,
                "hook": f"One prompt can make {topic} dramatically easier.",
                "archetype": "benefit"
            },
            {
                "score": 91,
                "hook": f"Most people are missing this part of {topic}.",
                "archetype": "curiosity_gap"
            },
            {
                "score": 90,
                "hook": f"Try this before doing {topic} manually.",
                "archetype": "challenge"
            }
        ]

def choose_hook(topic, angle, curiosity):
    candidates = generate_hooks(
        topic,
        angle,
        curiosity
    )
    history = load_hook_history()
    recent_hooks = get_recent_hooks(history)
    fresh = []
    blocked = []
    used_archetypes = []
    for item in candidates:
        hook = item["hook"]
        score = item["score"]
        archetype = item.get(
            "archetype",
            "unknown"
        )
        if is_recent_duplicate(
            hook,
            recent_hooks
        ):
            blocked.append(
                (hook, "duplicate")
            )
            continue
        if has_recent_pattern_repeat(
            hook,
            recent_hooks
        ):
            blocked.append(
                (hook, "pattern")
            )
            continue
        fresh.append(item)
    if not fresh:
        non_exact = [
            item
            for item in candidates
            if normalize_text(
                item["hook"]
            ) not in {
                normalize_text(old)
                for old in recent_hooks
            }
        ]
        if non_exact:
            fresh = non_exact
        else:
            fresh = candidates
    # Prefer the strongest candidate, but slightly reward
    # an archetype not used in the recent history.
    recent_archetypes = {
        str(item.get("archetype", "")).lower()
        for item in history[-8:]
        if isinstance(item, dict)
    }
    def final_score(item):
        bonus = 4 if (
            item.get("archetype", "")
            not in recent_archetypes
        ) else 0
        return item["score"] + bonus
    fresh.sort(
        reverse=True,
        key=final_score
    )
    selected = fresh[0]
    best_hook = selected["hook"]
    best_score = selected["score"]
    archetype = selected.get(
        "archetype",
        "unknown"
    )
    record_hook_usage(
        history,
        best_hook,
        best_score,
        archetype
    )
    print("=" * 60)
    print("SELECTED ELITE VIRAL HOOK")
    print("=" * 60)
    print(
        f"Score: {best_score:.1f}/100"
    )
    print(
        "Archetype:",
        archetype
    )
    print(
        "Hook:",
        best_hook
    )
    print(
        "Cooldown:",
        f"{HOOK_COOLDOWN} videos"
    )
    print(
        "Blocked:",
        len(blocked)
    )
    print("=" * 60)
    return best_hook
