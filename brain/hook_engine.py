from brain.ai_router import ask_ai
import json
import os
import re
from difflib import SequenceMatcher

HISTORY_FILE = "data/hook_history.json"
HOOK_COOLDOWN = 20
MAX_HISTORY = 100
SIMILARITY_THRESHOLD = 0.78

SYSTEM_PROMPT = """
You are the PromptProHub VIRAL HOOK ENGINE.
Your ONLY job is to create extremely strong short-form video hooks.
The hook is the FIRST sentence viewers hear.
Your goal is:
STOP THE SCROLL
CREATE CURIOSITY
PROMISE A SPECIFIC BENEFIT
MAKE THE VIEWER NEED TO KNOW WHAT HAPPENS NEXT

PromptProHub focuses on:
- AI prompts
- ChatGPT prompts
- Prompt templates
- AI productivity
- AI automation
- AI workflows
- AI tools
- AI for freelancers
- AI for creators
- AI for marketers
- AI for businesses
- AI digital products
- AI prompt ebooks and templates

The hook must connect directly to the topic.

================================
FORBIDDEN OPENINGS
================================

NEVER start with:
"What if you could..."
"What if..."
"Imagine..."
"Imagine having..."
"Have you ever wondered..."
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
"Have you ever..."

NEVER use generic motivational hooks.

NEVER use vague hooks such as:
"This changes everything."
"This is amazing."
"You need to see this."
"Nobody is ready for this."
unless the sentence contains a SPECIFIC reason
that creates curiosity.

================================
HOOK PATTERN DIVERSITY
================================

DO NOT repeatedly use the same opening structure.

Avoid repeatedly starting hooks with structures such as:
"You're wasting..."
"Most people..."
"Stop..."
"I tested..."
"I found..."
"This..."
"The problem..."

These structures may be used occasionally,
but do NOT let a batch become dominated by
one structure.

Across the 15 hooks, deliberately mix:
- pain
- curiosity
- contrast
- experiment
- mistake
- warning
- result
- specific audience
- challenge
- unexpected discovery
- practical shortcut
- hidden capability
- before/after
- specific time-saving
- specific business outcome

The hooks must feel like DIFFERENT ideas,
not the same sentence rewritten 15 times.

================================
STRONG HOOK PATTERNS
================================

Prefer hooks like:
"Watch me turn 10 hours of work into minutes."
"Most freelancers are using ChatGPT completely wrong."
"I tested this AI workflow so you don't have to."
"This ChatGPT prompt can save hours of repetitive work."
"I replaced an entire afternoon of work with one AI workflow."
"Stop writing these prompts from scratch."
"You're probably using ChatGPT backwards."
"I found the prompt that turns a blank page into a finished draft."
"This is how creators are cutting hours of work down to minutes."
"Most business owners don't know ChatGPT can do this."
"I tested 20 AI prompts. Only a few were actually useful."
"One prompt can turn your messy idea into a complete plan."
"The problem isn't ChatGPT. It's the way you're prompting it."

================================
IMPORTANT
================================

DO NOT invent fake achievements.

Never claim:
"I made $100,000"
"I made $1 million"
"I got 10,000 customers"
unless the topic or provided information actually proves it.

Use believable curiosity without making false claims.

================================
HOOK QUALITY
================================

Every hook should have at least ONE of:
- specific time saving
- money-saving angle
- productivity improvement
- surprising discovery
- common mistake
- hidden feature
- strong contrast
- specific problem
- curiosity gap
- unexpected result
- practical benefit

Whenever possible, make the benefit concrete.

Weak:
"AI is changing business."

Strong:
"Most business owners are still doing this manually."

================================
LENGTH
================================

Keep each hook between approximately
8 and 18 words.

Make it sound natural when spoken.

Do not write long explanations.

Generate 15 DIFFERENT hooks.

Then score each hook from 1-100 for:
- scroll_stopping_power
- curiosity
- specificity
- relevance
- benefit
- natural_sounding

Return ONLY valid JSON.

Format:
{
    "hooks": [
        {
            "hook": "Watch me turn 10 hours of work into minutes.",
            "scroll_stopping_power": 95,
            "curiosity": 92,
            "specificity": 94,
            "relevance": 96,
            "benefit": 95,
            "natural_sounding": 94
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
        history = history[-MAX_HISTORY:]
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
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
    first_normalized = normalize_text(first)
    second_normalized = normalize_text(second)
    if not first_normalized or not second_normalized:
        return 0.0
    return SequenceMatcher(None, first_normalized, second_normalized).ratio()

def get_hook_pattern(hook):
    words = word_list(hook)
    if not words:
        return ""
    return " ".join(words[:4])

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
    if similarity_score(first_stem, second_stem) >= 0.90:
        return True
    return False

def get_recent_hooks(history):
    return [
        item.get("hook", "")
        for item in history[-HOOK_COOLDOWN:]
        if isinstance(item, dict) and item.get("hook")
    ]

def is_recent_duplicate(hook, recent_hooks):
    normalized_hook = normalize_text(hook)
    for old_hook in recent_hooks:
        old_normalized = normalize_text(old_hook)
        if normalized_hook == old_normalized:
            return True
        if similarity_score(hook, old_hook) >= SIMILARITY_THRESHOLD:
            return True
    return False

def has_recent_pattern_repeat(hook, recent_hooks):
    for old_hook in recent_hooks:
        if same_opening_pattern(hook, old_hook):
            return True
    return False

def record_hook_usage(history, hook, score):
    import time
    history.append({
        "hook": hook,
        "score": round(float(score), 2),
        "pattern": get_hook_pattern(hook),
        "timestamp": time.time()
    })
    save_hook_history(history)
def generate_hooks(topic, angle, curiosity):
    history = load_hook_history()
    recent_hooks = get_recent_hooks(history)
    recent_examples = recent_hooks[-10:]
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
VIRAL ANGLE
================================

{angle}

================================
CURIOSITY
================================

{curiosity}

================================
RECENTLY USED HOOKS
================================

The following hooks were recently used.

DO NOT copy them.
DO NOT rewrite them with only minor wording changes.
DO NOT repeat their opening structure.

{recent_text}

================================
FINAL REQUIREMENT
================================

Create 15 highly specific hooks for this exact topic.

The 15 hooks must use DIFFERENT psychological
and linguistic patterns.

Do NOT create 15 variations of the same opening.

Prioritize concrete benefits and strong curiosity.

Remember:

NEVER use "What if you could..."
NEVER use "Imagine..."
NEVER use "Imagine having..."
NEVER use generic motivational openings.
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
        hooks = data.get("hooks", [])
        if not hooks:
            raise Exception("AI returned no hooks")
        cleaned_hooks = []
        for item in hooks:
            if not isinstance(item, dict):
                continue
            hook = str(
                item.get("hook", "")
            ).strip()
            if not hook:
                continue
            try:
                scores = [
                    float(item.get("scroll_stopping_power", 0)),
                    float(item.get("curiosity", 0)),
                    float(item.get("specificity", 0)),
                    float(item.get("relevance", 0)),
                    float(item.get("benefit", 0)),
                    float(item.get("natural_sounding", 0))
                ]
            except (TypeError, ValueError):
                continue
            average_score = sum(scores) / len(scores)
            cleaned_hooks.append(
                (
                    average_score,
                    hook
                )
            )
        if not cleaned_hooks:
            raise Exception(
                "No valid hooks remained after AI response parsing."
            )
        cleaned_hooks.sort(
            reverse=True,
            key=lambda item: item[0]
        )
        print("=" * 60)
        print("VIRAL HOOK ENGINE")
        print("=" * 60)
        print(
            f"Generated: {len(cleaned_hooks)} hooks"
        )
        print(
            f"Recently used hooks: {len(recent_hooks)}"
        )
        print("=" * 60)
        return cleaned_hooks
    except Exception as e:
        print("=" * 60)
        print("HOOK ENGINE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)
    return [
        (
            95,
            f"Most people are using {topic} the wrong way."
        ),
        (
            94,
            f"I found a faster way to handle {topic}."
        ),
        (
            93,
            f"This {topic} mistake can waste hours."
        ),
        (
            92,
            f"One simple change can make {topic} much easier."
        ),
        (
            91,
            f"I tested a better workflow for {topic}."
        ),
        (
            90,
            f"Stop doing {topic} manually."
        ),
        (
            89,
            f"This is why {topic} takes longer than it should."
        ),
        (
            88,
            f"The shortcut for {topic} is simpler than you think."
        )
    ]

def choose_hook(topic, angle, curiosity):
    hooks = generate_hooks(
        topic,
        angle,
        curiosity
    )
    if not hooks:
        return (
            f"Most people are using "
            f"{topic} the wrong way."
        )
    history = load_hook_history()
    recent_hooks = get_recent_hooks(history)
    fresh_hooks = []
    blocked_hooks = []
    for score, hook in hooks:
        if is_recent_duplicate(
            hook,
            recent_hooks
        ):
            blocked_hooks.append(
                (
                    score,
                    hook,
                    "near_duplicate"
                )
            )
            continue
        if has_recent_pattern_repeat(
            hook,
            recent_hooks
        ):
            blocked_hooks.append(
                (
                    score,
                    hook,
                    "repeated_pattern"
                )
            )
            continue
        fresh_hooks.append(
            (
                score,
                hook
            )
        )
    if fresh_hooks:
        best_score, best_hook = fresh_hooks[0]
    else:
        recent_normalized = {
            normalize_text(old_hook)
            for old_hook in recent_hooks
        }
        non_exact = [
            (
                score,
                hook
            )
            for score, hook in hooks
            if normalize_text(hook)
            not in recent_normalized
        ]
        if non_exact:
            best_score, best_hook = non_exact[0]
        else:
            best_score, best_hook = hooks[0]
            print(
                "WARNING: All generated hooks were recently used. "
                "Using highest-scoring fallback."
            )
    record_hook_usage(
        history,
        best_hook,
        best_score
    )
    print("=" * 60)
    print("SELECTED VIRAL HOOK")
    print("=" * 60)
    print(
        f"Score: {best_score:.1f}/100"
    )
    print(
        "Hook:",
        best_hook
    )
    print(
        "Hook cooldown:",
        f"{HOOK_COOLDOWN} videos"
    )
    print(
        "Blocked candidates:",
        len(blocked_hooks)
    )
    print("=" * 60)
    return best_hook
